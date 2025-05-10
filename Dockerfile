FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install postgres client so you get pg_isready
RUN apt-get update \
 && apt-get install -y --no-install-recommends postgresql-client \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project (or specify directories like "app", "alembic", and ".env")
COPY . /app/

# Expose port for FastAPI
EXPOSE 8000

# Run migrations then start the application via an entrypoint script
CMD ["/app/entrypoint.sh"]