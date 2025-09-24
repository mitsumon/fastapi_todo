FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Create workspaces directory structure
RUN mkdir -p /workspaces/todo-project
WORKDIR /workspaces/todo-project

# Copy requirements file (build context is set to parent directory in docker-compose.yml)
COPY requirements_full.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements_full.txt

# Ensure proper permissions
RUN chmod -R 755 /workspaces

ENV PYTHONUNBUFFERED=1

# Keep container running
CMD ["sleep", "infinity"]