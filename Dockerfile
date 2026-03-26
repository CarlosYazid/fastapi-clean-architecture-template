# / -- base image -- /
FROM python:3.13-slim AS base

RUN apt-get update

# configs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# / -- builder image -- /
FROM base AS builder

# uv configs
ENV UV_PROJECT_ENVIRONMENT=/app/.venv
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# uv
RUN pip install --no-cache-dir uv
ENV PATH="/root/.local/bin:/app/.venv/bin:$PATH"

# deps metadata
COPY src/pyproject.toml src/uv.lock* ./

# / ----------------------- Api ----------------------- /

# / -- dev builder -- /
FROM builder AS builder-api-dev
RUN uv sync --frozen --group dev

# / -- prod builder -- /
FROM builder AS builder-api-prod
RUN uv sync --no-dev --no-install-project

# / -- dev image -- /
FROM base AS api-dev

COPY --from=builder-api-dev /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY src src

ARG PORT=8080

EXPOSE ${PORT}

# / -- prod image -- /
FROM base AS api-prod

# no-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY --from=builder-api-prod /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY --chown=appuser:appgroup src src

COPY --chown=appuser:appgroup alembic.ini .

COPY --chown=appuser:appgroup migrations migrations

ARG PORT=8000

EXPOSE ${PORT}

USER appuser