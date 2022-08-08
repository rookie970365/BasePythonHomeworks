FROM python:3.10

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY fastapi-app .

EXPOSE 8000

CMD uvicorn main:app --host=0.0.0.0 --port=8000
