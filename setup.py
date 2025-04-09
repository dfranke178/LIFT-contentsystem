from setuptools import setup, find_packages

setup(
    name="lift-contentsystem",
    version="1.0.0",
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