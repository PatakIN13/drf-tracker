FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/usr/src/app

WORKDIR $APP_HOME

RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles

RUN pip install --upgrade pip
RUN apk add gcc musl-dev libffi-dev openssl-dev
RUN pip install poetry

COPY poetry.lock pyproject.toml $APP_HOME

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY ./app .

RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]