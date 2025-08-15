#!/usr/bin/env python3
"""
Startup script for the Voice Assistant application.

This script provides a convenient way to start the application with proper configuration.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_environment():
    """Check if the environment is properly configured."""
    env_file = project_root / ".env"
    if not env_file.exists():
        print("⚠️  Warning: .env file not found!")
        print("📋 Please copy env.example to .env and configure your API keys.")
        print("🔑 Required API keys:")
        print("   - ASSEMBLYAI_API_KEY")
        print("   - GEMINI_API_KEY") 
        print("   - MURF_API_KEY")
        print()
        
    # Check if virtual environment is active
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not activated!")
        print("🐍 Please activate your virtual environment:")
        print("   On Windows: .\\venv\\Scripts\\activate")
        print("   On Unix/Mac: source venv/bin/activate")
        print()

def main():
    """Main entry point."""
    print("🎙️  Starting AI Voice Assistant...")
    print("=" * 50)
    
    check_environment()
    
    try:
        import uvicorn
        from app.main import app, settings
        
        print(f"🚀 Starting server on {settings.host}:{settings.port}")
        print(f"🌐 Open your browser to: http://localhost:{settings.port}")
        print("🔄 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        uvicorn.run(
            "app.main:app",
            host=settings.host,
            port=settings.port,
            reload=settings.debug,
            log_level=settings.log_level.lower()
        )
        
    except ImportError as e:
        print(f"❌ Error: Missing dependency - {e}")
        print("📦 Please install dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
