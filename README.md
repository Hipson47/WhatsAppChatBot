# 🤖 Telegram RAG Multi-Agent Bot

A production-ready, RAG-powered multi-agent Telegram chatbot built with Python and Google Cloud AI Platform. This advanced bot leverages retrieval-augmented generation (RAG) and multi-agent architecture to provide intelligent, context-aware conversational AI through Telegram's Bot API.

## ✨ Key Features xd

- **🚀 Production-Ready**: Fully containerized with Docker and Google Cloud Run deployment
- **🧠 RAG-Powered**: Advanced retrieval-augmented generation for contextual responses
- **🤖 Multi-Agent Architecture**: Specialized agents for different conversation contexts
- **🔍 Vector Search**: ChromaDB integration for intelligent knowledge retrieval
- **📱 Telegram Native**: Seamless integration through Telegram Bot API
- **🛡️ Enterprise Security**: Rate limiting, input validation, and secure credential management
- **☁️ Cloud Native**: Optimized for Google Cloud Run with advanced CI/CD pipeline
- **📊 Structured Logging**: Professional logging with structured output for monitoring
- **🔧 Developer Experience**: Modern Python architecture with comprehensive tooling

## 🛠️ Tech Stack xd

### Core Framework
- **Backend**: Python 3.11+ with python-telegram-bot library
- **Bot Framework**: Telegram Bot API with polling
- **Architecture**: Agent-based system with RAG-powered tools and LangChain orchestration

### AI & Machine Learning  
- **LLM Integration**: OpenAI GPT-4o-mini for conversational responses
- **Embeddings**: Google Cloud Vertex AI (textembedding-gecko@003)
- **Vector Database**: ChromaDB for embeddings storage
- **RAG Framework**: LangChain with conversational retrieval chains

### Communication & APIs
- **Messaging**: Telegram Bot API
- **HTTP Client**: httpx for async operations
- **Bot Library**: python-telegram-bot v20+
- **Data Validation**: Pydantic v2

### Infrastructure & Deployment
- **Containerization**: Multi-stage Docker builds
- **Cloud Platform**: Google Cloud Run
- **CI/CD**: Google Cloud Build with Artifact Registry
- **Secret Management**: Google Secret Manager
- **Monitoring**: Structured logging with structlog

### Development & Testing
- **Package Management**: pip with version constraints
- **Code Quality**: Type hints and comprehensive validation
- **Local Development**: Docker Compose with hot reload

## 🏗️ Production Architecture

### 🔄 Automated RAG Pipeline with GCS

This project implements a **production-grade, automated RAG pipeline** with Google Cloud Storage (GCS) as the persistent storage backend. The architecture decouples the knowledge base from the application container, enabling scalable, automated deployments.

#### 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTOMATED RAG PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📚 Knowledge Base     ➜    ☁️ GCS Storage     ➜    🤖 Bot      │
│                                                                 │
│  1. Local Processing   │   2. Automated Upload  │  3. Runtime    │
│  • Load documents      │   • Cloud Build runs   │  • Download    │
│  • Create embeddings   │   • ingest.py script   │  • from GCS    │
│  • Build vector store  │   • Upload to bucket   │  • on startup  │
│                       │                        │               │
└─────────────────────────────────────────────────────────────────┘
```

#### 🚀 Key Benefits

**🏗️ Infrastructure Scalability:**
- ✅ **Stateless containers** - No dependency on local storage
- ✅ **Horizontal scaling** - Multiple instances share same knowledge base
- ✅ **Zero-downtime deployments** - New versions download updated knowledge
- ✅ **Cloud-native storage** - Leverages GCS durability and performance

**⚡ Automated Operations:**
- ✅ **CI/CD Integration** - Knowledge base automatically processed during build
- ✅ **Version control** - Knowledge base versioned with application code
- ✅ **No manual steps** - Complete automation from code to production
- ✅ **Consistent deployments** - Same knowledge base across all environments

**💰 Cost Optimization:**
- ✅ **Storage efficiency** - GCS cold storage for infrequently accessed data
- ✅ **Compute optimization** - Knowledge processing only during builds
- ✅ **Resource sharing** - Single knowledge base serves multiple instances

#### 🔧 Architecture Components

**1. Build-Time Processing (`ingest.py`):**
```python
# During Cloud Build:
# 1. Load documents from knowledge_base/
# 2. Create vector embeddings using Vertex AI
# 3. Build ChromaDB vector store locally
# 4. Upload entire vector store to GCS bucket
```

**2. Runtime Download (`startup.sh`):**
```bash
# During container startup:
# 1. Check if vector store exists locally
# 2. Download from GCS bucket if needed
# 3. Launch application with ready knowledge base
```

**3. GCS Bucket Structure:**
```
gs://{project-id}-knowledge-base/
└── vector_store/
    ├── chroma.sqlite3
    ├── index/
    │   └── [embeddings data]
    └── [additional ChromaDB files]
```

#### 📋 Required Google Cloud Setup

**Storage Bucket Permissions:**
```bash
# Grant Cloud Run service account access to GCS
export PROJECT_ID="vortex-ai-user"
export SERVICE_ACCOUNT_EMAIL="chatbot-runtime-sa@${PROJECT_ID}.iam.gserviceaccount.com"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role="roles/storage.objectAdmin"
```

**Automatic Bucket Creation:**
The `ingest.py` script automatically creates the GCS bucket `{project-id}-knowledge-base` if it doesn't exist.

## 📁 Project Structure

```
WhatsAppChatBot/
├── src/                       # Main application source code
│   ├── bots/                 # Telegram bot implementation (UI layer)
│   │   ├── __init__.py
│   │   └── telegram_bot.py   # Clean interface that delegates to agents
│   ├── agents/               # Agent system components (AI logic layer)
│   │   ├── __init__.py
│   │   └── main_agent.py     # Core RAG agent with LangChain tools
│   ├── core/                 # Shared utilities and configurations
│   │   ├── __init__.py
│   │   └── vector_store.py   # Vector database management
│   ├── tools/                # Agent tools and external integrations
│   │   ├── __init__.py
│   │   └── datetime_tools.py # Time retrieval tools
│   ├── prompts/              # Prompt templates and management
│   │   └── __init__.py
│   └── __init__.py
├── knowledge_base/           # RAG knowledge storage
├── tests/                    # Test suite
├── backend/                  # Legacy backend (to be migrated)
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── Dockerfile               # Multi-stage container build
├── docker-compose.yml       # Local development setup
├── cloudbuild.yaml         # Google Cloud Build config
├── .env.example            # Environment template
├── .gitignore             # Git ignore rules
├── .cursorrules           # Development guidelines
└── README.md              # This file
```

### Directory Roles

- **`src/`**: Main application code organized by domain
- **`src/bots/`**: Telegram bot UI layer - handles user interactions and delegates to agents
- **`src/agents/`**: Multi-agent orchestration and agent definitions
- **`src/core/`**: Shared utilities, configurations, and base classes
- **`src/tools/`**: Reusable tools for agents (datetime, web search, calculations, etc.)
- **`src/prompts/`**: Prompt templates and prompt management
- **`knowledge_base/`**: RAG knowledge storage and vector databases
- **`tests/`**: Comprehensive test suite for all components

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**: For local development
- **Docker & Docker Compose**: For containerized development  
- **Google Cloud Account**: For production deployment and AI services
- **Telegram Bot Token**: From BotFather for Telegram API access
- **Google Cloud AI Platform**: For Vertex AI integration

### Development Requirements

- **Git**: Version control
- **Google Cloud SDK**: For deployment and testing
- **ngrok** (optional): For local webhook testing

### Quick Start (Local Development)

1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd WhatsAppChatBot
   ```

2. **Set up Python environment** (Alternative to Docker):
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file in the project root with the following content:
   ```env
   # Telegram Bot Configuration
   TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
   
   # OpenAI API Configuration
   OPENAI_API_KEY=your_openai_api_key
   
   # Google Cloud AI Platform
   GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
   GOOGLE_CLOUD_PROJECT=your-project-id
   
   # Configuration
   ENVIRONMENT=development
   LOG_LEVEL=info
   ```
   
   **💡 Tip:** You can also create a `.env.example` file with empty values as a template for other users.
   
   **Getting Required API Keys:**
   
   **Telegram Bot Token:**
   1. Message [@BotFather](https://t.me/botfather) on Telegram
   2. Send `/newbot` and follow the instructions
   3. Copy the bot token and add it to your `.env` file
   
   **OpenAI API Key:**
   1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
   2. Create a new API key
   3. Copy the key (starts with `sk-`) and add it to your `.env` file

## 🔐 Google Cloud Authentication Setup

To build the knowledge base (`ingest.py`), the application needs to authenticate with Google Cloud to use the Vertex AI embedding models.

### 1. Create a Service Account
- Go to the [IAM & Admin -> Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts) page in your Google Cloud project
- Click **"+ CREATE SERVICE ACCOUNT"**
- Give it a name (e.g., `chatbot-embedder`) and click **"CREATE AND CONTINUE"**
- Grant it the **"Vertex AI User"** role
- Click **"DONE"**

### 2. Create a JSON Key
- Find the newly created service account in the list
- Click on the three dots under "Actions" and select **"Manage keys"**
- Click **"ADD KEY"** -> **"Create new key"**
- Select **JSON** as the key type and click **"CREATE"**
- A JSON file will be downloaded to your computer. **Treat this file like a password!**

### 3. Configure Environment Variable
- Move the downloaded JSON file to a secure location on your computer (e.g., a folder like `C:\gcloud-keys\`)
- Open your `.env` file
- Set the `GOOGLE_APPLICATION_CREDENTIALS` variable to the **full path** of the downloaded JSON file. For example:
  ```env
  GOOGLE_APPLICATION_CREDENTIALS="C:\gcloud-keys\my-project-12345-abcdef123456.json"
  ```

Now, when you run `start.bat`, the `ingest.py` script will be able to authenticate with Google Cloud successfully.

4. **Launch the application** (Windows):
   ```bash
   # Use the intelligent startup script (recommended)
   start.bat
   ```
   
   The `start.bat` script will:
   - ✅ Check if your `.env` file is properly configured
   - ✅ Verify Google Cloud authentication setup
   - ✅ Handle knowledge base creation/updates automatically
   - ✅ Start the Telegram bot
   
   **Alternative (manual launch):**
   ```bash
   # First time: Build knowledge base
   python ingest.py
   
   # Then start the bot
   python main.py
   ```

5. **Test the bot**:
   - Find your bot on Telegram using the username you created with BotFather
   - Send `/start` to begin chatting
   - Try these example queries:
     - *"What time is it in Tokyo?"*
     - Ask questions about your knowledge base documents
     - The bot provides intelligent answers with quality assurance!

## 📚 Managing the Knowledge Base

The bot uses a Retrieval-Augmented Generation (RAG) system to provide intelligent responses based on your knowledge base. To update the bot's knowledge:

### Setting up Google Cloud Authentication

Before you can process your knowledge base, you need to set up Google Cloud authentication for the Vertex AI embeddings:

1. **Create a Google Cloud Service Account**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Navigate to IAM & Admin > Service Accounts
   - Create a new service account with Vertex AI permissions

2. **Download the service account key**:
   - Generate and download a JSON key file for your service account
   - Save it securely on your local machine

3. **Set the environment variable**:
   ```bash
   # Add this to your .env file
   GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
   ```

### Processing Your Knowledge Base

1. **Add documents to the knowledge base**:
   - Place your documents (`.txt`, `.md` files) in the `knowledge_base/` directory
   - The system supports text files and Markdown documents
   - PDF support is available through the unstructured library

2. **Run the ingestion script**:
   ```bash
   # Process all documents and create the vector store
   python ingest.py
   ```

3. **What happens during ingestion**:
   - Documents are loaded from the `knowledge_base/` directory
   - Text is split into manageable chunks (1000 characters with 100 character overlap)
   - Embeddings are created using Google's Vertex AI embedding model
   - All data is stored locally in a ChromaDB vector store (`vector_store/` directory)

### Notes:
- The `knowledge_base/` and `vector_store/` directories are excluded from version control
- You need to re-run `python ingest.py` whenever you add or modify documents
- The vector store is created locally and doesn't require external database services

## 🔧 Extending the Agent System

The Parse-Execute-Supervise architecture makes it incredibly easy to add new capabilities. We've demonstrated this by adding a **time retrieval tool** to showcase the modularity.

### ⏰ **Example: Time Retrieval Tool (Already Implemented)**

The bot can now handle requests like:
- *"What time is it?"* (returns UTC time)
- *"What time is it in Tokyo?"* (returns time in Asia/Tokyo timezone)
- *"Current time in Europe/Warsaw"* (returns time in Polish timezone)

### 📋 **How to Add New Capabilities**

To add a new command, follow this proven 4-step pattern:

### 1. Define the Command Model
Add a new Pydantic model in `src/core/models.py`:
```python
class WebSearch(BaseModel):
    task: Literal["web_search"] = "web_search"
    query: str = Field(..., description="Search query for the web")
    max_results: int = Field(5, description="Number of results to return")

# Don't forget to update the Union!
AgentCommand = Union[SearchKnowledgeBase, GetCurrentTime, WebSearch]
```

### 2. Create the Tool
Create a new file in `src/tools/` or add to existing ones:
```python
# src/tools/web_tools.py
from langchain.tools import tool

@tool
def web_search(query: str, max_results: int = 5) -> str:
    """Search the web for current information."""
    # Your implementation here
    return search_results
```

### 3. Update the Parser
Modify the parser prompt in `parse_command` function:
```python
parser_prompt = f"""
Available tasks:
1. 'search_knowledge_base': For questions about provided documents
2. 'get_current_time': For current time requests
3. 'web_search': For current information not in the knowledge base
...
"""
```

### 4. Update the Executor
Add handling in `execute_command`:
```python
elif isinstance(command, WebSearch):
    return web_search.run(command.query, command.max_results)
```

### ✅ **Benefits of This Pattern**

- **Type Safety**: Pydantic validation ensures data integrity
- **Modular**: Each tool is independent and reusable
- **Quality Assured**: Every response goes through supervision
- **Extensible**: Add unlimited capabilities without touching existing code
- **Testable**: Each component can be tested in isolation

This pattern ensures type safety, clear intent understanding, and maintainable code growth.

## 🚀 Production Deployment

### 🔄 Automated RAG Pipeline Deployment

The new architecture provides **fully automated deployment** with integrated knowledge base processing. No manual steps required!

#### 1. **One-Time Google Cloud Setup**

**🔧 Enable Required APIs:**
   ```bash
# Authenticate and set project
   gcloud auth login
gcloud config set project vortex-ai-user
   
   # Enable required APIs
   gcloud services enable run.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
```

**🔑 Configure Secrets:**
```bash
# Store API keys in Google Secret Manager
echo -n "your_telegram_bot_token" | gcloud secrets create TELEGRAM_BOT_TOKEN --data-file=-
echo -n "your_openai_api_key" | gcloud secrets create OPENAI_API_KEY --data-file=-

# Store service account credentials as JSON
gcloud secrets create GOOGLE_APPLICATION_CREDENTIALS_JSON --data-file=path/to/service-account-key.json
```

**👤 Grant Storage Permissions (REQUIRED):**
   ```bash
# Grant the runtime service account access to GCS
export PROJECT_ID="vortex-ai-user"
export SERVICE_ACCOUNT_EMAIL="chatbot-runtime-sa@${PROJECT_ID}.iam.gserviceaccount.com"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role="roles/storage.objectAdmin"
```

#### 2. **🚀 Automated Deployment**

**Single Command Deployment:**
   ```bash
# Deploy with automated knowledge base processing
gcloud builds submit --config cloudbuild.yaml
```

**🔄 What Happens Automatically:**
1. **📦 Build Container** - Docker image with application + gcloud CLI
2. **📚 Process Knowledge Base** - Run `ingest.py` to create vector embeddings
3. **☁️ Upload to GCS** - Store vector database in `{project-id}-knowledge-base` bucket
4. **🚀 Deploy to Cloud Run** - Launch service with GCS download capability

#### 3. **📊 Deployment Pipeline Features**

**✅ Zero-Configuration Knowledge Base:**
- ✅ **Automatic processing** during build
- ✅ **GCS upload** with bucket auto-creation
- ✅ **Runtime download** on container startup
- ✅ **Version synchronization** with application code

**⚡ Optimized for Production:**
- ✅ **Fast container startup** - GCS download in parallel with health checks
- ✅ **Stateless architecture** - Multiple instances share same knowledge base
- ✅ **Automatic scaling** - Cloud Run handles traffic spikes
- ✅ **Zero-downtime updates** - New versions seamlessly replace old ones

**🔒 Enterprise Security:**
- ✅ **Secret Manager integration** - No hardcoded credentials
- ✅ **IAM-based access** - Principle of least privilege
- ✅ **Service account isolation** - Separate accounts for build vs runtime
- ✅ **Encrypted storage** - GCS encryption at rest and in transit

### 🚀 **Cloud Run Optimization**

The application is optimized for Cloud Run with:
- **Lazy Initialization**: Fast startup for health checks (< 1 second)
- **On-Demand Loading**: Heavy AI models load only when needed
- **Health Check Ready**: Passes readiness probes without timeouts
- **Cold Start Optimized**: Minimal initialization overhead

### Environment Variables

The application supports the following environment variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `TELEGRAM_BOT_TOKEN` | Bot token from BotFather | - | Yes |
| `OPENAI_API_KEY` | OpenAI API key for GPT-4o-mini | - | Yes |
| `GOOGLE_CLOUD_PROJECT` | GCP Project ID | - | Yes |
| `GOOGLE_APPLICATION_CREDENTIALS` | Service account key path | - | Yes (for RAG) |
| `ENVIRONMENT` | Environment type | development | No |
| `LOG_LEVEL` | Logging level | info | No |

## 🏗️ Architecture

### Agent-Based System

The application uses a clean agent-based architecture with clear separation of concerns:

**Architecture Layers:**
- **UI Layer** (`src/bots/`): Telegram bot interface - handles user interactions
- **Agent Layer** (`src/agents/`): Intelligent agents with tools and reasoning capabilities
- **Core Layer** (`src/core/`): Shared utilities, vector store management, and data processing

**Current Agent Implementation:**
- **Parse-Execute-Supervise Pattern**: Three-step process with quality assurance
- **Lazy Initialization**: Fast startup with on-demand component loading for Cloud Run
- **Parser LLM**: Converts natural language to structured Pydantic commands  
- **Command Models** (`models.py`): Type-safe command definitions with validation
- **Multi-Tool Executor**: Handles different command types with appropriate tools
- **Supervisor Layer**: Quality control and answer correction before user delivery
- **Current Capabilities**:
  - **Knowledge Base Search**: RAG-powered answers from your documents
  - **Time Retrieval**: Current time in any timezone worldwide
- **Extensible Design**: Easy to add new commands and tools

**Parse-Execute-Supervise Pattern:**

The system now uses a sophisticated three-step approach with quality assurance:

1. **Parse Step**: Natural language input → Structured Pydantic command
   - Uses a specialized parser LLM (temperature=0 for consistency)
   - Converts user intent into type-safe, validated command objects
   - Enables precise understanding of user requirements

2. **Execute Step**: Structured command → Tool execution → Initial response
   - Routes commands to appropriate executors
   - Uses specialized agent with relevant tools
   - Generates contextual responses based on tool results

3. **Supervise Step**: Initial response → Quality review → Final response
   - Uses a dedicated supervisor LLM (temperature=0.1 for balanced evaluation)
   - Reviews answers for relevance, accuracy, completeness, and clarity
   - Either approves the original answer or provides an improved version
   - **Evaluation Criteria:**
     - **Relevance**: Does the answer directly address the user's query?
     - **Accuracy**: Is the information correct and consistent?
     - **Completeness**: Are all key details included?
     - **Clarity**: Is the answer easy to understand?

**Lazy Initialization Pattern:**

For optimal Cloud Run performance, the system uses lazy loading:

- **Fast Startup**: Application starts in milliseconds for health checks
- **On-Demand Loading**: AI components load only on first user request
- **Memory Efficient**: Avoids loading heavy models during deployment
- **Health Check Friendly**: Passes Cloud Run readiness probes quickly
- **Production Optimized**: Reduces cold start penalties

**Benefits of Parse-Execute-Supervise:**
- **Quality Assurance**: Every response is reviewed before reaching the user
- **Error Correction**: Supervisor can fix inaccurate or incomplete answers
- **Intent Alignment**: Ensures responses directly address user queries
- **Consistency**: Standardized quality criteria across all responses
- **Type Safety**: Pydantic models ensure command validation
- **Clarity**: Clear separation between understanding, execution, and quality control
- **Debuggability**: Easy to inspect parsed commands, execution paths, and quality reviews
- **Extensibility**: Add new commands without touching existing logic
- **Cloud Native**: Optimized for serverless deployments with lazy initialization

**Benefits of Agent Architecture:**
- **Modularity**: Clean separation between UI (Telegram) and AI logic (agents)
- **Extensibility**: Add new tools and capabilities without changing the bot interface
- **Testability**: Agent logic can be tested independently of the Telegram interface
- **Reusability**: Agents can be used by different interfaces (web, API, CLI)
- **Scalability**: Agent processing can be moved to separate services if needed

### RAG Implementation

- **Knowledge Ingestion**: Automatic document processing and chunking
- **Vector Storage**: ChromaDB for efficient similarity search
- **Embedding Generation**: Sentence Transformers for semantic understanding
- **Context Retrieval**: Smart context selection for improved responses

### Security Features

- **Rate Limiting**: Prevents abuse with configurable limits
- **Input Validation**: Comprehensive input sanitization and validation
- **Authentication**: Secure API key management
- **Logging**: Structured logging without exposing sensitive data

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test categories
python -m pytest tests/test_api.py
python -m pytest tests/test_agents.py
python -m pytest tests/test_rag.py
```

## 📊 Monitoring & Observability

The application includes comprehensive monitoring capabilities:

- **Structured Logging**: JSON-formatted logs for easy parsing
- **Health Checks**: Docker health checks and API endpoints
- **Metrics**: Request metrics and performance monitoring
- **Tracing**: Distributed tracing support (future enhancement)

## 🗺️ Project Roadmap

### Phase 1: Core RAG Implementation ✅
- [x] Multi-agent architecture foundation
- [x] RAG system with vector search
- [x] Production deployment pipeline
- [x] Security and rate limiting

### Phase 2: Enhanced Intelligence 🚧
- [ ] Advanced agent routing algorithms
- [ ] Context-aware conversation memory
- [ ] Multi-modal support (images, documents)
- [ ] Custom agent creation API

### Phase 3: Enterprise Features 📋
- [ ] Multi-tenant architecture
- [ ] Advanced analytics dashboard
- [ ] A/B testing for agent responses
- [ ] Integration with popular CRM systems

### Phase 4: Platform Expansion 🔮
- [ ] Discord and WhatsApp integration
- [ ] Voice message support
- [ ] Real-time collaboration features
- [ ] Mobile companion app

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow our coding standards (see `.cursorrules`)
4. Write tests for your changes
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Documentation**: [Wiki](https://github.com/yourusername/WhatsAppChatBot/wiki)
- **Issues**: [Issue Tracker](https://github.com/yourusername/WhatsAppChatBot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/WhatsAppChatBot/discussions)
- **Email**: support@yourproject.com

---

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by developers who believe AI should be accessible and powerful.