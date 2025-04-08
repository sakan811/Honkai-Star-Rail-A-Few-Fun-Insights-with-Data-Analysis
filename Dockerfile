FROM python:3.13.2-alpine3.21 as builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy only what's needed for dependency installation first
COPY uv.lock pyproject.toml /app/

# Install dependencies first (this layer can be cached)
WORKDIR /app
RUN uv sync --frozen --no-dev --no-cache --no-install-project

# Now copy the rest of the project code
COPY . /app/

# Final stage with only necessary files
FROM python:3.13.2-alpine3.21
WORKDIR /app

# Copy the virtual environment and all app files
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1

# Expose the Flask port
EXPOSE 1234

# Run the Flask server by default
CMD ["gunicorn", "--bind", "0.0.0.0:1234", "main:app"]