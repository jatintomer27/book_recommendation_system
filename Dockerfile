FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV STREAMLIT_LOG_LEVEL=debug

COPY src/ src/
COPY requirements.txt .
COPY pyproject.toml .
COPY README.md .
COPY LICENSE .

# -------------------------------
# Install Python dependencies
# -------------------------------
RUN pip install --upgrade pip \
    && pip install -r requirements.txt 

COPY . .

# -------------------------------
# Install project as a package
# (VERY IMPORTANT for -m usage)
# -------------------------------
RUN pip3 install -r requirements.txt
RUN pip install .

# -------------------------------
# Expose the ports
# -------------------------------
EXPOSE 8501

# -------------------------------
# Default command: Run full DVC pipeline
# -------------------------------

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--logger.level=info"]
