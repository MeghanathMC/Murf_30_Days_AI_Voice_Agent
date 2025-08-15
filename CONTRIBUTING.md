# Contributing to AI Voice Assistant

Thank you for your interest in contributing to the AI Voice Assistant project! This document provides guidelines and instructions for contributors.

## 🤝 Getting Started

### Prerequisites
- Python 3.12 or higher
- Git
- A modern web browser
- API keys for AssemblyAI, Google Gemini, and Murf AI

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/ai-voice-assistant.git
   cd ai-voice-assistant
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Unix/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

5. **Run the Application**
   ```bash
   python run.py
   ```

## 📝 Code Style

### Python Code Standards
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Add docstrings to all modules, classes, and functions
- Keep line length under 88 characters (Black formatter standard)

### Project Structure
```
app/
├── config/          # Configuration and settings
├── schemas/         # Pydantic models for validation
├── services/        # External service integrations
└── main.py         # Main FastAPI application
```

### Code Organization Principles
- **Single Responsibility**: Each module should have one clear purpose
- **Dependency Injection**: Services should be injected, not imported directly
- **Error Handling**: Always provide graceful fallbacks
- **Logging**: Use structured logging with appropriate levels

## 🔧 Development Guidelines

### Adding New Features

1. **Service Integration**
   - Add new services in `app/services/`
   - Follow the pattern established by existing services
   - Include proper error handling and logging

2. **API Endpoints**
   - Add new endpoints in `app/main.py`
   - Use Pydantic schemas for request/response validation
   - Include proper HTTP status codes and error responses

3. **Frontend Changes**
   - Modify files in `static/` directory
   - Maintain responsive design principles
   - Test across different browsers

### Code Quality

1. **Type Safety**
   ```python
   # Good
   def process_text(text: str, max_length: int = 3000) -> str:
       return text[:max_length]
   
   # Avoid
   def process_text(text, max_length=3000):
       return text[:max_length]
   ```

2. **Error Handling**
   ```python
   # Good
   try:
       result = service.call_api()
       return ApiResponse(success=True, data=result)
   except ApiException as e:
       logger.error(f"API call failed: {e}")
       return ApiResponse(success=False, error=str(e))
   
   # Avoid
   result = service.call_api()  # No error handling
   ```

3. **Logging**
   ```python
   # Good
   logger.info(f"Processing request for session: {session_id}")
   logger.error(f"Failed to transcribe audio: {error}")
   
   # Avoid
   print("Processing request")  # Use logging instead
   ```

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest httpx pytest-asyncio

# Run tests
pytest tests/
```

### Writing Tests
- Write unit tests for all service classes
- Include integration tests for API endpoints
- Test error conditions and edge cases
- Maintain test coverage above 80%

## 📋 Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Follow the coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new voice processing feature"
   ```

4. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format
Follow conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

## 🐛 Bug Reports

When reporting bugs, please include:
- **Environment**: OS, Python version, browser
- **Steps to Reproduce**: Clear step-by-step instructions
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Logs**: Relevant error messages or logs
- **API Keys**: Confirm which APIs are configured

## 💡 Feature Requests

For new features:
- Check existing issues first
- Describe the use case clearly
- Explain the expected behavior
- Consider implementation complexity
- Discuss potential breaking changes

## 📚 Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Update API documentation in schemas
- Include examples for new features

## 🎯 Areas for Contribution

### High Priority
- [ ] Add unit tests for service classes
- [ ] Implement Redis for session storage
- [ ] Add voice activity detection
- [ ] Improve error messages and user feedback

### Medium Priority
- [ ] Add support for multiple languages
- [ ] Implement voice cloning features
- [ ] Add conversation export functionality
- [ ] Performance optimizations

### Low Priority
- [ ] Mobile app companion
- [ ] Custom voice training
- [ ] Advanced conversation analytics
- [ ] Integration with other AI services

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: [your-email@example.com] for private inquiries

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing to the AI Voice Assistant! 🎙️✨
