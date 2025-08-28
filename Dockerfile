From python:3.11-slim

RUN apt-get update

ENV POETRY_VERSION=1.8.3 \
    PATH="/opt/poetry/bin:$PATH"

RUN   curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["poetry", "run", "python", "-m", "src.my_vacation.main"]