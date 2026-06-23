# ── Stage 1: Builder ──────────────────────────────────────────
FROM python:3.9-slim AS builder

# Set working directory
WORKDIR /app

# Copy only requirements first (for better layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Stage 2: Runner ───────────────────────────────────────────
FROM python:3.9-slim AS runner

# Set working directory
WORKDIR /app

# Create a non-root user and group
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

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
