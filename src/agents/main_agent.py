"""
Main Agent Module for RAG-powered Conversational AI.

This module implements an agent-based architecture using LangChain tools
and agents to handle user queries through the knowledge base.
"""

import os
import logging
from langchain_community.vectorstores import Chroma
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools.retriever import create_retriever_tool

# Configure logging
logger = logging.getLogger(__name__)

# --- CONSTANTS ---
VECTOR_STORE_DIR = "vector_store"

# --- VALIDATION ---
if not os.path.exists(VECTOR_STORE_DIR):
    logger.error(f"Vector store directory '{VECTOR_STORE_DIR}' not found.")
    logger.error("Please run 'python ingest.py' first to create the knowledge base.")
    raise FileNotFoundError(f"Vector store not found at {VECTOR_STORE_DIR}")

# --- INITIALIZATION ---
logger.info("Initializing RAG agent components...")

# Initialize embeddings model (must match the one used in ingest.py)
embeddings = VertexAIEmbeddings(model_name="textembedding-gecko@003")

# Load the persistent vector store
db = Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": 5})  # Retrieve top 5 most relevant chunks

# Initialize the Chat Model for answering questions
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)

# Create the primary tool for the agent: the knowledge base retriever
retriever_tool = create_retriever_tool(
    retriever,
    "knowledge_base_search",
    "Searches and returns information from the user's knowledge base. Use this for any questions about the provided documents."
)

tools = [retriever_tool]

# Get the prompt template for the agent
# This prompt instructs the agent on how to use the available tools
prompt = hub.pull("hwchase17/openai-tools-agent")

# Create the agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create the agent executor, which runs the agent's reasoning loop
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

logger.info("RAG agent initialized successfully.")


def process_query(user_input: str) -> str:
    """
    Processes a user query using the RAG agent.
    
    This function serves as the main interface between the Telegram bot
    and the agent-based RAG system.
    
    Args:
        user_input (str): The user's question or query
        
    Returns:
        str: The agent's response based on the knowledge base
    """
    try:
        logger.info(f"Processing query: {user_input}")
        response = agent_executor.invoke({"input": user_input})
        answer = response.get("output", "I could not find an answer.")
        logger.info("Query processed successfully")
        return answer
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        return "I'm sorry, I encountered an error while processing your request."