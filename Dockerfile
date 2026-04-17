FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set workspace
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files
COPY . .

# Set environment variables (Placeholders)
ENV API_ID="" \
    API_HASH="" \
    BOT_TOKEN="" \
    ADMIN_ID="0"

# Run the bot
CMD ["python", "bot.py"]
