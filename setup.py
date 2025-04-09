from setuptools import setup, find_packages

setup(
    name="linkedin-content-system",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.109.0",
        "uvicorn==0.27.0",
        "gunicorn>=21.2.0",
        "python-multipart==0.0.6",
        "pydantic==2.5.0",
        "python-dotenv==1.0.0",
        "requests==2.31.0"
    ],
) 