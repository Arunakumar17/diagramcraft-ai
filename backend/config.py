import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "diagramcraft")
    OUTPUT_DIR: str = os.path.join(os.path.dirname(__file__), "output")
    TEMP_DIR: str = os.path.join(os.path.dirname(__file__), "output", "temp")
    
    # Ensure directories exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

settings = Settings()
