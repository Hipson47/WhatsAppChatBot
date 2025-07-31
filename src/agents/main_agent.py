"""
Main Agent Module with Parse-Execute-Supervise Architecture.

This module implements a three-step agent system:
1. Parse: Convert natural language input into structured commands
2. Execute: Run the appropriate tools based on the parsed command  
3. Supervise: Review and potentially correct the output for quality assurance
"""

import os
import logging
from typing import List, Union
from pydantic import BaseModel

from langchain_community.vectorstores import Chroma
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain import hub

from src.core.models import AgentCommand, SearchKnowledgeBase, GetCurrentTime
from src.tools.datetime_tools import get_current_time

# --- CONFIGURATION ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# --- CONSTANTS ---
VECTOR_STORE_DIR = "vector_store"

# --- VALIDATION ---
if not os.path.exists(VECTOR_STORE_DIR):
    logger.error(f"Vector store directory '{VECTOR_STORE_DIR}' not found.")
    logger.error("Please run 'python ingest.py' first to create the knowledge base.")
    raise FileNotFoundError(f"Vector store not found at {VECTOR_STORE_DIR}")

# --- INITIALIZATION ---
logger.info("Initializing AI components for the agent...")

# 1. Initialize models
# Model for parsing user intent into a structured command
parser_llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0).with_structured_output(AgentCommand)

# Model for executing the task and generating a final answer
executor_llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)

# Model for supervising and quality control of outputs
supervisor_llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.1)  # A dedicated model for quality control

# 2. Initialize Retriever Tool
embeddings = VertexAIEmbeddings(model_name="textembedding-gecko@003")
db = Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": 5})

knowledge_base_tool = create_retriever_tool(
    retriever,
    "knowledge_base_search",
    "Searches and returns information from the user's knowledge base. Use this for any questions that require context from provided documents."
)
tools = [knowledge_base_tool, get_current_time]

# 3. Create the Executor Agent
# This agent's job is to use tools to fulfill a specific task
executor_prompt = hub.pull("hwchase17/openai-tools-agent")
agent = create_tool_calling_agent(executor_llm, tools, executor_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

logger.info("Agent components initialized.")


# --- CORE AGENT LOGIC ---

def parse_command(user_input: str) -> BaseModel:
    """
    Parses the user's natural language input into a structured Pydantic model command.
    
    Args:
        user_input (str): The user's natural language query
        
    Returns:
        BaseModel: A structured command object based on the user's intent
    """
    logger.info(f"Parsing command for input: '{user_input}'")
    
    parser_prompt = f"""
    Given the user's request, determine the appropriate task and its parameters.
    
    Available tasks:
    1. 'search_knowledge_base': Use this when the user is asking a question or looking for information that might be in the provided documents. The 'query' should be the user's question.
    2. 'get_current_time': Use this when the user asks for the current time. The 'timezone' parameter is optional and defaults to UTC, but if the user specifies a city or timezone (e.g., "time in Warsaw", "what time is it in New York"), extract it.

    User Request: "{user_input}"
    
    Now, provide the output in the required JSON format.
    """
    
    command = parser_llm.invoke(parser_prompt)
    logger.info(f"Parsed command: {command.dict()}")
    return command


def execute_command(command: BaseModel) -> str:
    """
    Executes a parsed command using the appropriate tools.
    
    Args:
        command (BaseModel): A structured command object to execute
        
    Returns:
        str: The result of executing the command
    """
    logger.info(f"Executing command: {command.dict()}")
    
    if isinstance(command, SearchKnowledgeBase):
        # If the task is to search the knowledge base, invoke the agent executor with the query
        result = agent_executor.invoke({"input": command.query})
        return result.get("output", "I could not find an answer.")
    
    elif isinstance(command, GetCurrentTime):
        # If the task is to get the current time, call the tool directly
        # This is more efficient than running the full agent executor for a simple task
        return get_current_time.run(command.timezone)
        
    else:
        logger.warning(f"Unknown command type: {type(command)}")
        return "I'm not sure how to handle that request."


def supervise_output(original_query: str, generated_answer: str) -> str:
    """
    Reviews the generated answer for quality and alignment with the original query.
    
    This function acts as a quality assurance layer that ensures responses:
    - Directly address the user's query
    - Are accurate and consistent  
    - Provide complete information
    - Are clear and understandable
    
    Args:
        original_query (str): The user's original question
        generated_answer (str): The answer generated by the executor
        
    Returns:
        str: Either the approved original answer or an improved version
    """
    logger.info(f"Supervising output for query: '{original_query}'")
    logger.info(f"Initial answer: '{generated_answer}'")

    supervisor_prompt = f"""
    You are a Quality Assurance Supervisor. Your task is to review an answer generated by an AI agent based on a user's original query.

    Original User Query: "{original_query}"
    
    Generated Answer to Review: "{generated_answer}"

    Please evaluate the answer based on the following criteria:
    1.  **Relevance:** Does the answer directly address the user's query?
    2.  **Accuracy:** Is the information correct and consistent with the query?
    3.  **Completeness:** Does it fully answer the user's question without leaving out key details?
    4.  **Clarity:** Is the answer easy to understand?

    If the answer is satisfactory, respond ONLY with the word "APPROVED".
    If the answer is unsatisfactory, DO NOT say it's wrong. Instead, provide a corrected and improved version of the answer directly, without any preamble.
    """
    
    supervisor_feedback = supervisor_llm.invoke(supervisor_prompt).content
    
    if supervisor_feedback.strip().upper() == "APPROVED":
        logger.info("Supervisor approved the original answer.")
        return generated_answer
    else:
        logger.warning(f"Supervisor revised the answer. New answer: '{supervisor_feedback}'")
        return supervisor_feedback


def process_query(user_input: str) -> str:
    """
    Full end-to-end processing: parse, execute, and supervise.
    
    This is the main entry point called by the Telegram bot.
    Implements the Parse-Execute-Supervise pattern for robust, quality-assured query handling.
    
    Args:
        user_input (str): The user's natural language query
        
    Returns:
        str: The agent's quality-assured response
    """
    try:
        # Step 1: Parse the user input into a structured command
        parsed_command = parse_command(user_input)
        
        # Step 2: Execute the parsed command
        initial_answer = execute_command(parsed_command)
        
        # Step 3: Supervise and quality-check the answer
        final_answer = supervise_output(user_input, initial_answer)
        
        return final_answer
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        return "I'm sorry, an error occurred while processing your request."