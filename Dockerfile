FROM python:3.10

COPY . ./app

WORKDIR /app

RUN pip install requests datetime

CMD ["python","src/main.py"]