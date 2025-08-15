# 🎙️ AI Voice Assistant

A sophisticated voice-powered conversational AI assistant built with FastAPI, featuring real-time speech-to-text, AI-powered responses, and natural text-to-speech synthesis. Experience seamless voice interactions with cutting-edge AI technology.

**✨ Recently Refactored (Day 14)** - Now featuring modular architecture, type-safe APIs, and production-ready code structure!

![Voice Assistant Demo](https://via.placeholder.com/800x400/0ea5e9/ffffff?text=AI+Voice+Assistant+Demo)

## 🌟 Features

### 🎤 Voice Processing
- **Real-time Speech Recognition** - Powered by AssemblyAI for accurate transcription
- **Natural Language Understanding** - Google Gemini 2.5 Flash for intelligent responses
- **High-Quality Text-to-Speech** - Murf AI for lifelike voice synthesis
- **Session Management** - Persistent conversation history across interactions

### 🎨 Modern User Interface
- **Responsive Design** - Beautiful, mobile-first interface
- **Real-time Status Updates** - Visual feedback for all processing stages
- **Conversation History** - Persistent chat display with message management
- **Accessibility Features** - Keyboard shortcuts and ARIA labels

### 🏗️ Production-Ready Architecture
- **Modular Design** - Clean separation of concerns with service layer
- **Type Safety** - Comprehensive Pydantic schemas for all APIs
- **Error Handling** - Graceful fallbacks with structured error responses
- **Configuration Management** - Environment-based settings with validation
- **Structured Logging** - Comprehensive logging with configurable levels
- **Audio Processing** - WebM format with opus codec for optimal quality
- **Secure File Handling** - Temporary uploads with automatic cleanup
- **Cross-platform Support** - Works on Windows, macOS, and Linux

## 🛠️ Technology Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework for building APIs
- **[AssemblyAI](https://www.assemblyai.com/)** - Advanced speech-to-text API
- **[Google Gemini](https://ai.google.dev/)** - Large language model for intelligent responses
- **[Murf AI](https://murf.ai/)** - Professional text-to-speech synthesis
- **[Python 3.12+](https://python.org/)** - Core programming language

### Frontend
- **Vanilla JavaScript** - Modern ES6+ features for optimal performance
- **CSS3** - Advanced styling with custom properties and animations
- **WebRTC APIs** - Real-time audio capture and processing
- **Progressive Web App** - Responsive design principles

### Key Dependencies
```python
fastapi>=0.116.1          # Web framework
assemblyai>=0.42.1        # Speech-to-text
google-generativeai>=0.8.5 # AI language model
httpx>=0.28.1             # Async HTTP client
python-dotenv>=1.1.1      # Environment management
uvicorn>=0.35.0           # ASGI server
pydantic>=2.11.7          # Data validation and settings
pydantic-settings>=2.0.0  # Settings management
python-multipart>=0.0.20  # File upload handling
```

## 🏗️ Architecture

### Modular Backend Structure
```
ai-voice-assistant/
├── app/
│   ├── config/
│   │   └── settings.py         # Environment configuration
│   ├── schemas/
│   │   └── api_schemas.py      # Pydantic models
│   ├── services/
│   │   ├── stt_service.py      # AssemblyAI integration
│   │   ├── llm_service.py      # Google Gemini integration
│   │   └── tts_service.py      # Murf AI integration
│   └── main.py                 # FastAPI application
├── static/                     # Frontend assets
├── main.py                     # Application entry point
└── run.py                      # Development startup script
```

### System Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI        │    │   External      │
│   (Web App)     │    │   Backend        │    │   Services      │
│                 │    │                  │    │                 │
│ ┌─────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ │ Voice UI    │◄├────┤►│ API Routes   │◄├────┤►│ AssemblyAI  │ │
│ │ - Recording │ │    │ │ + Schemas    │ │    │ │ (STT)       │ │
│ │ - Playback  │ │    │ │ + Validation │ │    │ │             │ │
│ └─────────────┘ │    │ └──────────────┘ │    │ └─────────────┘ │
│                 │    │        │         │    │                 │
│ ┌─────────────┐ │    │ ┌──────▼──────┐ │    │ ┌─────────────┐ │
│ │ Chat UI     │◄├────┤►│ Service Layer│◄├────┤►│ Google      │ │
│ │ - Messages  │ │    │ │ - STT/LLM/TTS│ │    │ │ Gemini      │ │
│ │ - History   │ │    │ │ - Error Handling │  │ │ (LLM)       │ │
│ └─────────────┘ │    │ └──────────────┘ │    │ └─────────────┘ │
│                 │    │        │         │    │                 │
│                 │    │ ┌──────▼──────┐ │    │ ┌─────────────┐ │
│                 │    │ │ Config &    │ │    │ │ Murf AI     │ │
│                 │    │ │ Logging     │ │    │ │ (TTS)       │ │
│                 │    │ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Data Flow
1. **Audio Capture** → User speaks into microphone (WebRTC)
2. **Upload** → Audio sent to FastAPI backend as WebM file
3. **Transcription** → AssemblyAI converts speech to text
4. **AI Processing** → Google Gemini generates intelligent response
5. **Speech Synthesis** → Murf AI converts response to natural audio
6. **Playback** → Browser plays AI response audio
7. **Continuation** → Automatic re-recording for seamless conversation

## 🚀 Quick Start

### Prerequisites
- Python 3.12 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Microphone access
- Internet connection for API services

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-voice-assistant.git
cd ai-voice-assistant
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Copy the example environment file and configure your API keys:

```bash
# Copy template
cp env.example .env

# Edit .env with your API keys
```

Required API keys in `.env`:
```env
# Required API Keys
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
GEMINI_API_KEY=your_google_gemini_api_key_here
MURF_API_KEY=your_murf_api_key_here

# Optional Configuration
PORT=8000
HOST=0.0.0.0
DEBUG=False
LOG_LEVEL=INFO
```

### 5. Run the Application
```bash
# Quick start (recommended)
python run.py

# Alternative: Direct uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Access the Application
Open your browser and navigate to:
```
http://localhost:8000
```

## 🔑 API Keys Setup

### AssemblyAI (Speech-to-Text)
1. Visit [AssemblyAI Console](https://www.assemblyai.com/app)
2. Create an account and get your API key
3. Add to `.env`: `ASSEMBLYAI_API_KEY=your_key_here`

### Google Gemini (Language Model)
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Add to `.env`: `GEMINI_API_KEY=your_key_here`

### Murf AI (Text-to-Speech)
1. Visit [Murf AI Console](https://murf.ai/dashboard)
2. Subscribe to a plan and get your API key
3. Add to `.env`: `MURF_API_KEY=your_key_here`

## 📡 API Documentation

### Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve main application |
| `/health` | GET | Health check and API status |
| `/llm/query` | POST | Single voice query with AI response |
| `/agent/chat/{session_id}` | POST | Conversational chat with history |
| `/agent/chat/{session_id}` | DELETE | Clear session history |
| `/transcribe/file` | POST | Audio transcription only |
| `/tts/echo` | POST | Echo transcribed audio with TTS |
| `/tts` | POST | Text to speech conversion |

### Detailed API Usage

#### Agent Chat (Recommended)
```bash
curl -X POST "http://localhost:8000/agent/chat/my-session-123" \
  -F "file=@recording.webm"
```

**Response:**
```json
{
  "session_id": "my-session-123",
  "audio_url": "https://murf.ai/audio/...",
  "transcription": "Hello, how are you?",
  "llm_response": "I'm doing well, thank you! How can I help you today?",
  "history_length": 2,
  "error": null
}
```

#### Text-to-Speech Only
```bash
curl -X POST "http://localhost:8000/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, world!"}'
```

## 🔧 Development

### Project Structure
```
ai-voice-assistant/
├── app/                   # Main application package
│   ├── config/
│   │   └── settings.py    # Configuration management
│   ├── schemas/
│   │   └── api_schemas.py # Pydantic models
│   ├── services/
│   │   ├── stt_service.py # Speech-to-text service
│   │   ├── llm_service.py # Language model service
│   │   └── tts_service.py # Text-to-speech service
│   └── main.py            # FastAPI application
├── static/                # Frontend assets
│   ├── index.html         # Main application UI
│   ├── script.js          # Voice assistant logic
│   └── style.css          # Modern CSS styling
├── temp_uploads/          # Temporary audio files
├── main.py                # Application entry point
├── run.py                 # Development startup script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from env.example)
└── README.md             # This file
```

### Adding New Features
1. **New API Endpoints** - Add routes in `app/main.py` with proper schemas
2. **New Services** - Create service classes in `app/services/`
3. **Configuration** - Add settings in `app/config/settings.py`
4. **Data Models** - Define Pydantic schemas in `app/schemas/`
5. **Frontend Features** - Modify files in `static/`
6. **Error Handling** - Extend fallback responses and error handlers

### Development Best Practices
- **Type Safety** - Use Pydantic models for all API endpoints
- **Service Layer** - Abstract external API calls into service classes
- **Configuration** - Use environment variables for all settings
- **Logging** - Add structured logging for debugging and monitoring
- **Error Handling** - Provide graceful fallbacks for all failure scenarios

### Running Tests
```bash
# Install test dependencies
pip install pytest httpx

# Run tests
pytest tests/
```

## 📊 Performance & Limitations

### Performance Metrics
- **Transcription Latency:** ~2-3 seconds (AssemblyAI)
- **AI Response Time:** ~1-2 seconds (Gemini 2.5 Flash)
- **TTS Generation:** ~3-4 seconds (Murf AI)
- **Total Response Time:** ~6-9 seconds end-to-end

### Current Limitations
- **Text Length:** Murf AI enforces 3000 character limit
- **Audio Format:** WebM with Opus codec required
- **Browser Support:** Modern browsers only (WebRTC required)
- **Network Dependency:** All AI processing requires internet connection

### Recent Improvements (Day 14 Refactoring)
- [x] **Modular Architecture** - Clean separation of concerns
- [x] **Type Safety** - Comprehensive Pydantic schemas
- [x] **Service Layer** - Abstracted external API integrations
- [x] **Configuration Management** - Environment-based settings
- [x] **Enhanced Logging** - Structured logging with file output
- [x] **Better Error Handling** - Graceful fallbacks and user feedback
- [x] **Production Ready** - Improved code quality and maintainability

### Planned Improvements
- [ ] Comprehensive test suite
- [ ] Redis for session storage
- [ ] Real-time streaming for faster responses
- [ ] Additional voice options and languages
- [ ] Custom AI model fine-tuning
- [ ] Mobile app companion
- [ ] Docker containerization

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Follow the modular architecture** - Use services, schemas, and proper configuration
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Commit changes** (`git commit -m 'feat: add amazing feature'`)
7. **Push to branch** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

### Development Setup
```bash
# Clone and setup
git clone <your-fork>
cd ai-voice-assistant
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env with your API keys

# Run application
python run.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AssemblyAI** for providing excellent speech-to-text capabilities
- **Google** for the powerful Gemini language model
- **Murf AI** for high-quality text-to-speech synthesis
- **FastAPI** team for the amazing web framework
- **Open Source Community** for inspiration and support

## 📞 Support & Contact

- **GitHub Issues:** [Report bugs or request features](https://github.com/yourusername/ai-voice-assistant/issues)
- **Documentation:** [Full API Documentation](https://yourusername.github.io/ai-voice-assistant)
- **Email:** your.email@example.com

---

<div align="center">
  <strong>Built with ❤️ using modern AI technologies</strong>
  <br>
  <sub>Star ⭐ this repository if you found it helpful!</sub>
</div>
