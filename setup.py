#!/usr/bin/env python
from setuptools import setup, find_packages
import os
import subprocess
import sys

# Install packages
setup(
    name="lift-content-system",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "python-multipart>=0.0.6",
        "pydantic>=1.10.0,<2.0.0",
        "python-dotenv==1.0.0",
        "gunicorn==21.2.0"
    ],
    python_requires=">=3.8",
)

# Download NLTK data
import nltk
nltk.download('punkt')
nltk.download('stopwords')

# Download spaCy model
subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])

print("Setup completed successfully!") 