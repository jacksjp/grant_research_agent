# Use Python 3.12 slim image for smaller size
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry: Don't create virtual environment, install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port for Streamlit
EXPOSE 8501

# Health check for the Streamlit app
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Set environment variables for Google Cloud
ENV GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Default command to run the Streamlit app
CMD ["poetry", "run", "streamlit", "run", "grant_research_app_simple.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
