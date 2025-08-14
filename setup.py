#!/usr/bin/env python3
"""
Setup script for the Intelligent Engine Maintenance Assistant.
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def create_directories():
    """Create necessary project directories."""
    directories = [
        "data",
        "data/raw",
        "data/raw/maintenance_manuals",
        "data/raw/dot_regulations", 
        "data/processed",
        "data/synthetic",
        "data/chroma_db",
        "logs"
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    print("✅ Created project directories")


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        import langchain
        import chromadb
        import google.generativeai
        import pandas
        import plotly
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False


def create_env_file():
    """Create .env file if it doesn't exist."""
    if not Path('.env').exists():
        print("📝 Creating .env file...")
        print("Please update the .env file with your Google AI Studio API key!")
        if Path('.env.example').exists():
            shutil.copy('.env.example', '.env')
        else:
            # Create basic .env file
            env_content = """# Google AI Studio Configuration
GOOGLE_API_KEY=your_google_ai_studio_api_key_here
GEMINI_MODEL=gemini-pro
EMBEDDING_MODEL=models/embedding-001

# Vector Database Configuration  
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
CHROMA_COLLECTION_NAME=maintenance_docs

# Application Configuration
STREAMLIT_PORT=8501
LOG_LEVEL=INFO
MAX_QUERY_LENGTH=500
MAX_RESULTS=10
"""
            with open('.env', 'w') as f:
                f.write(env_content)
        print("✅ Created .env file from template")
    else:
        print("ℹ️  .env file already exists")


def main():
    """Main setup function."""
    print("🚚 Setting up Intelligent Engine Maintenance Assistant...")
    print("=" * 60)

    # Create directories
    create_directories()

    # Create env file
    create_env_file()

    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Update .env file with your Google AI Studio API key")
    print("3. Run: python initialize_db.py")
    print("4. Run: streamlit run src/streamlit_app.py")
    print("\nGet your Google AI Studio API key at:")
    print("https://makersuite.google.com/app/apikey")
    print("=" * 60)


if __name__ == "__main__":
    main()
