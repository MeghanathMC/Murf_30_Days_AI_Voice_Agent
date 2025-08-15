# 🎙️ AI Voice Assistant

A sophisticated voice-powered conversational AI assistant built with FastAPI, featuring real-time speech-to-text, AI-powered responses, and natural text-to-speech synthesis. Experience seamless voice interactions with cutting-edge AI technology.

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

### 🔧 Robust Architecture
- **Error Handling** - Graceful fallbacks for all API failures
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
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI        │    │   External      │
│   (Web App)     │    │   Backend        │    │   APIs          │
│                 │    │                  │    │                 │
│ ┌─────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ │ Voice UI    │◄├────┤►│ Audio Routes │◄├────┤►│ AssemblyAI  │ │
│ │ - Recording │ │    │ │ - /transcribe │ │    │ │ (STT)       │ │
│ │ - Playback  │ │    │ │ - /tts       │ │    │ │             │ │
│ └─────────────┘ │    │ └──────────────┘ │    │ └─────────────┘ │
│                 │    │                  │    │                 │
│ ┌─────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ │ Chat UI     │◄├────┤►│ Agent Routes │◄├────┤►│ Google      │ │
│ │ - Messages  │ │    │ │ - /agent/chat│ │    │ │ Gemini      │ │
│ │ - History   │ │    │ │ - /llm/query │ │    │ │ (LLM)       │ │
│ └─────────────┘ │    │ └──────────────┘ │    │ └─────────────┘ │
│                 │    │                  │    │                 │
│                 │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│                 │    │ │ Static Files │ │    │ │ Murf AI     │ │
│                 │    │ │ - HTML/CSS   │ │    │ │ (TTS)       │ │
│                 │    │ │ - JavaScript │ │    │ │             │ │
│                 │    │ └──────────────┘ │    │ └─────────────┘ │
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
Create a `.env` file in the project root:

```env
# Required API Keys
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
GEMINI_API_KEY=your_google_gemini_api_key_here
MURF_API_KEY=your_murf_api_key_here

# Optional Configuration
PORT=8000
HOST=0.0.0.0
DEBUG=False
```

### 5. Run the Application
```bash
# Development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn main:app --host 0.0.0.0 --port 8000
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
| `/llm/query` | POST | Single voice query with AI response |
| `/agent/chat/{session_id}` | POST | Conversational chat with history |
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
├── main.py                 # FastAPI application
├── static/                 # Frontend assets
│   ├── index.html         # Main application UI
│   ├── script.js          # Voice assistant logic
│   └── style.css          # Modern CSS styling
├── temp_uploads/          # Temporary audio files
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md             # This file
```

### Adding New Features
1. **New API Endpoints** - Add routes in `main.py`
2. **Frontend Features** - Modify files in `static/`
3. **AI Models** - Update model configurations in respective API functions
4. **Error Handling** - Extend fallback responses and error handlers

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

### Planned Improvements
- [ ] Offline fallback capabilities
- [ ] Additional voice options and languages
- [ ] Real-time streaming for faster responses
- [ ] Custom AI model fine-tuning
- [ ] Mobile app companion

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit changes** (`git commit -m 'Add amazing feature'`)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
black main.py
flake8 main.py

# Run type checking
mypy main.py
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
