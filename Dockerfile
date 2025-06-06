FROM python:3.11-slim

# System dependencies for ML and Streamlit
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port Heroku expects
EXPOSE 8080

# Streamlit needs this env var for Heroku
ENV PORT=8080

# Run the app
CMD ["streamlit", "run", "chat_app.py", "--server.port=8080", "--server.address=0.0.0.0"] 