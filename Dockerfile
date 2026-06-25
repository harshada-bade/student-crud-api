# ── Stage 1: Builder ──────────────────────────────────────────
FROM python:3.9-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11.23 /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy lockfile and project metadata first (for better layer caching)
COPY pyproject.toml uv.lock ./

# Install runtime dependencies into a virtual environment
RUN uv sync --frozen --no-dev --no-install-project

# ── Stage 2: Runner ───────────────────────────────────────────
FROM python:3.9-slim AS runner

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user and group
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Copy the virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY . .

RUN chown -R appuser:appuser /app

USER appuser 

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "run.py"]
