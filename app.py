import os
import logging
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("app")

# Import and start the actual application
from src.api.minimal_webhook import app

if __name__ == "__main__":
    import uvicorn
    
    # Download NLTK data
    try:
        import nltk
        logger.info("Downloading NLTK punkt data...")
        nltk.download('punkt', quiet=True)
        logger.info("Downloading NLTK stopwords data...")
        nltk.download('stopwords', quiet=True)
        logger.info("NLTK data downloaded successfully")
    except Exception as e:
        logger.error(f"Error downloading NLTK data: {str(e)}")

    # Download spaCy model
    try:
        import spacy
        from spacy.cli import download
        logger.info("Checking for spaCy en_core_web_sm model...")
        try:
            # First check if the model is installed
            if not spacy.util.is_package("en_core_web_sm"):
                logger.info("Downloading spaCy en_core_web_sm model...")
                download("en_core_web_sm")
                logger.info("spaCy model downloaded successfully")
            else:
                logger.info("spaCy en_core_web_sm model already exists")
            
            # Now load the model
            nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model loaded successfully")
        except Exception as e:
            logger.error(f"Error with spaCy model loading: {str(e)}")
    except Exception as e:
        logger.error(f"Error with spaCy model: {str(e)}")
    
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting application on port {port}")
    uvicorn.run("app:app", host="0.0.0.0", port=port) 