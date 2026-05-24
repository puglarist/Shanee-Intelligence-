FROM python:3.11-slim

WORKDIR /app

# Install Poetry and configure to not use virtualenv in container
RUN pip install poetry && poetry config virtualenvs.create false

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-dev

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
