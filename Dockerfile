FROM python:3.13.2-alpine3.21
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

# Expose the Flask port
EXPOSE 1234

# Run the Flask server by default
CMD ["python", "main.py", "--mode=server", "--host=0.0.0.0", "--port=5000"]