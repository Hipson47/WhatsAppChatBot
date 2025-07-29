# WhatsApp AI Chatbot Builder

A powerful, locally-run application that enables anyone to create their own intelligent WhatsApp chatbot powered by OpenAI's advanced language models and custom knowledge bases. Simply add your documents (PDFs, text files), configure your API keys, and let your bot provide intelligent, context-aware responses to WhatsApp messages using Retrieval-Augmented Generation (RAG) technology.

## ✨ Key Features

- **🚀 Easy Setup** - No technical expertise required! Our automated script handles everything from environment setup to webhook configuration
- **📱 WhatsApp Integration** - Seamless integration with WhatsApp through the reliable Twilio API
- **🤖 AI-Powered Responses** - Leverage OpenAI's `gpt-4o-mini` model for intelligent, human-like conversations
- **📚 Custom Knowledge Base** - Upload your PDF and TXT files to create a personalized knowledge base using RAG (Retrieval-Augmented Generation)
- **⚡ Automated Configuration** - Fully automated webhook setup with Twilio - no manual configuration needed
- **🏗️ Modular Architecture** - Clean, extensible codebase following best practices for easy customization and scaling
- **☁️ Production Ready** - Built with enterprise-grade deployment capabilities for Google Cloud Run
- **🔒 Security First** - Environment-based configuration keeps your API keys and sensitive data secure

## 🛠️ Tech Stack

- **Backend Framework:** Python 3.11 + FastAPI
- **Web Server:** Uvicorn (ASGI server)
- **Messaging Platform:** Twilio API for WhatsApp integration
- **AI/ML:** OpenAI GPT-4o-mini for natural language processing
- **Knowledge Base:** LlamaIndex for document processing and retrieval
- **Vector Database:** ChromaDB for efficient similarity search
- **Containerization:** Docker with multi-stage builds
- **Cloud Deployment:** Google Cloud Run with CI/CD pipeline
- **Development:** Hot-reload development server with comprehensive logging

## 📋   Prerequisites

Before getting started, ensure you have the following installed on your machine:

- **Python 3.10 or higher** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Twilio Account** - [Sign up for free](https://www.twilio.com/try-twilio)
- **OpenAI API Account** - [Get your API key](https://platform.openai.com/api-keys)

## 🚀 Installation & Quick Start

Follow these simple steps to get your WhatsApp AI chatbot up and running:

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/WhatsAppChatBot.git
cd WhatsAppChatBot
```

### Step 2: Configure Environment Variables
1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```
2. Open the `.env` file in a text editor and fill in your API credentials:
   ```env
   # Twilio Credentials (from your Twilio Console)
   TWILIO_ACCOUNT_SID=your_account_sid_here
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_PHONE_NUMBER=whatsapp:+14155238886

   # OpenAI API Key (from your OpenAI account)
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Step 3: Prepare Your Knowledge Base
1. Create a `documents` folder in the project root: 
   ```bash
   mkdir documents
   ```
2. Add your PDF and TXT files to this folder. These will become your bot's knowledge base.

### Step 4: Launch Your Bot
Simply double-click the `start.bat` file, or run it from the command line:
```bash
start.bat
```

**That's it!** The script will automatically:
- Set up a Python virtual environment
- Install all required dependencies
- Start the FastAPI server
- Configure ngrok for webhook tunneling
- Update your Twilio webhook settings
- Display your bot's public URL

## 📱 How to Use

1. **Connect to Twilio Sandbox:**
   - Send a WhatsApp message to your Twilio Sandbox number (typically `+1 415 523 8886`)
   - Follow the instructions to join the sandbox (usually sending a specific code)

2. **Start Chatting:**
   - Once connected, send any message to your bot
   - The bot will search through your uploaded documents and provide intelligent responses
   - Ask questions related to your knowledge base for the most accurate answers

3. **Monitor Activity:**
   - Check the console output to see incoming messages and bot responses
   - All interactions are logged for debugging and monitoring

## 🗺️ Project Roadmap

We're continuously working to make this chatbot builder even more powerful and user-friendly:

- **🖥️ Desktop GUI Application** - User-friendly Electron + React interface for non-technical users
- **📁 Drag-and-Drop Interface** - Easy file upload and knowledge base management
- **🌐 Multi-Platform Support** - Integration with Discord, Telegram, and other messaging platforms
- **📊 Conversation Dashboard** - View chat history, analytics, and bot performance metrics
- **🧠 Advanced AI Features** - Support for custom AI models and fine-tuning capabilities
- **🔄 Real-time Updates** - Hot-swap knowledge base updates without restarting the bot
- **👥 Multi-User Support** - Handle multiple users and conversation contexts simultaneously
- **📈 Analytics & Insights** - Detailed usage statistics and conversation analysis

## 🏗️ Architecture

This project follows modern software architecture principles:

- **Microservices Design** - Modular components for easy maintenance and scaling
- **Async/Await Pattern** - Non-blocking I/O for high performance
- **Type Safety** - Full type hints and Pydantic validation throughout
- **Production Ready** - Docker containerization and Cloud Run deployment
- **Security Best Practices** - Environment-based secrets and secure API handling

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, your help makes this project better for everyone.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- **Documentation:** Check our [Wiki](https://github.com/yourusername/WhatsAppChatBot/wiki) for detailed guides
- **Issues:** Report bugs or request features in our [Issue Tracker](https://github.com/yourusername/WhatsAppChatBot/issues)
- **Discussions:** Join the community in [GitHub Discussions](https://github.com/yourusername/WhatsAppChatBot/discussions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. This means you're free to use, modify, and distribute this software for personal or commercial purposes.

---

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by developers who believe AI should be accessible to everyone. 