FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY Pipfile Pipfile.lock /code/

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

COPY . /code/

RUN chmod +x /code/entrypoint.sh

ENTRYPOINT ["sh", "/code/entrypoint.sh"]
