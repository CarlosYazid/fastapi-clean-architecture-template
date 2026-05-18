# / -- base image -- /
FROM python:3.13-slim AS base

# FIX: Ejecutar apt-get update + upgrade en el mismo RUN para aplicar
# los parches de seguridad disponibles del OS (sed, openssl, zlib, etc.)
# y limpiar la caché para reducir tamaño de imagen.
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

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

# FIX: Usar uv directamente desde su imagen oficial en lugar de instalarlo
# via pip, para evitar las vulnerabilidades de pip (CVE-2026-3219, CVE-2026-6357, CVE-2026-1703)
# y no dejar pip en la imagen final.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

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
# FIX: Deshabilitar pip en el venv de producción para eliminar
# sus vulnerabilidades de la imagen final (CVE-2026-3219, CVE-2026-6357)
RUN /app/.venv/bin/python -m pip uninstall pip -y 2>/dev/null || true

# / -- dev image -- /
FROM base AS api-dev

COPY --from=builder-api-dev /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY src src

ARG PORT=8080

EXPOSE ${PORT}

# / -- prod image -- /
# FIX: Cambiar de python:3.13-slim (Debian 13) a cgr.dev/chainguard/python:latest
# para obtener parches de seguridad del SO más actualizados,
# o bien usar una imagen distroless/chainguard para eliminar la superficie de ataque del OS. 
FROM cgr.dev/chainguard/python:latest AS api-prod

# configs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

COPY --from=builder-api-prod /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY --chown=65532:65532 src src
COPY --chown=65532:65532 alembic.ini .
COPY --chown=65532:65532 migrations migrations

ARG PORT=8000

EXPOSE ${PORT}

USER 65532