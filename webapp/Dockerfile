FROM python:3.6.4

RUN pip3 install pipenv

COPY Pipfile* /app/

WORKDIR /app

RUN pipenv install --system --dev
COPY . /app

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
