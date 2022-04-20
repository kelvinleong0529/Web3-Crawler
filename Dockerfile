FROM python:3

COPY . /app

WORKDIR /app

RUN pipenv install

CMD ["python","Production/main.py"]