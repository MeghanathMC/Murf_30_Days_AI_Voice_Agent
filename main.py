"""
Entry point for the Voice Assistant application.

This module serves as the main entry point and imports the refactored application.
"""

from app.main import app, settings

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
