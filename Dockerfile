FROM python:3.12-slim
WORKDIR /app

# Copy of metadata and dependencies
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock

# Install uv
RUN pip install --upgrade pip \
    && pip install uv

# Install dependencies
RUN uv sync

# Copy over rest of project
COPY . .

# Expose web application port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=helpdesk_manager.main
ENV FLASK_RUN_HOST=0.0.0.0

# Run web application
CMD ["uv", "run", "main.py"]
