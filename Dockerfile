FROM python:3.13-slim-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create workdir
WORKDIR /app

# Copy only project files needed to install dependencies
COPY pyproject.toml uv.lock ./

# Install libpq-dev and build tools
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install dependencies
RUN uv sync --frozen

# Now copy the rest of the app
COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
