ARG PYTHON
FROM python:3.9

WORKDIR /workspace

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . .

ENV UV_PROJECT_ENVIRONMENT=/usr/local
RUN uv sync --frozen --no-cache --all-extras

CMD ["nettowel", "help"]