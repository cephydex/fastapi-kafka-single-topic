# update to use python-slim and minimize image size for better mgt (startup time) and efficiency
FROM python:3.10

RUN pip install pipenv

WORKDIR /app
COPY Pipfile* ./


RUN pipenv install

COPY . /app

EXPOSE 8000
ENTRYPOINT ["pipenv"]
CMD [ "run", "server", "--reload"]