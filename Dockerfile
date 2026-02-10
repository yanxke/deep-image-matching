FROM ubuntu:22.04

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON=3.11
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libgl1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace/dim

# Copy dependency metadata only first to maximize layer cache reuse.
COPY pyproject.toml uv.lock ./

# Install third-party dependencies before copying the full source tree.
RUN uv sync --dev --no-install-project

# Copy local source code.
COPY . .

# Install the local project itself (usually quick if deps are already cached).
RUN uv sync --dev

# Run tests.
RUN uv run pytest
