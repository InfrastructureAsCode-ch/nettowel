ARG PYTHON
FROM python:3.9

WORKDIR /workspace

ENV PATH="/root/.poetry/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install curl -y \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
    && poetry config virtualenvs.create false

COPY . .

RUN poetry install --no-dev --extras full --no-interaction --no-ansi

CMD ["nettowel", "help"]