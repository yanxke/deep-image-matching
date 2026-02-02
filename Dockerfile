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
    git \
    ca-certificates \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libgl1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace/dim

# Clone repo
ARG BRANCH=master
RUN git clone https://github.com/3DOM-FBK/deep-image-matching.git . && \
    git checkout ${BRANCH}

# Install dependencies using uv
# This will install Python and all dependencies in pyproject.toml
RUN uv sync --dev

# Running the tests:
RUN uv run pytest
