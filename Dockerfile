FROM python:3.10

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN pip install --upgrade pip &&\
    pip install --no-cache-dir poetry==1.8.5

ENV PATH="/root/.local/bin:$PATH"

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-dev --no-interaction --no-ansi

COPY . .

CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
