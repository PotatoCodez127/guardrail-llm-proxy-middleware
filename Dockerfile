# Dockerfile
FROM python:3.10-slim as builder

WORKDIR /build
COPY pyproject.toml .
COPY src/ src/

# Build wheel package
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -e .

FROM python:3.10-slim

WORKDIR /app
# Establish non-root execution context for security
RUN useradd -m -s /bin/bash proxyuser

COPY --from=builder /build/wheels /wheels
COPY pyproject.toml .
COPY src/ src/
COPY examples/ examples/

RUN pip install --no-cache-dir pydantic pydantic-settings ollama python-dotenv && \
    pip install --no-cache-dir /wheels/*

USER proxyuser

# Default configurations; overridden via docker run -e
ENV OLLAMA_API_BASE_URL="http://host.docker.internal:11434"
ENV PRIMARY_MODEL="gemma4:31b-cloud"
ENV JUDGE_MODEL="gemma4:31b-cloud"

CMD ["python", "examples/async_proxy_implementation.py"]