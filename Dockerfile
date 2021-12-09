FROM python:3

RUN sudo apt-get update && apt-get upgrade && apt-get autoremove && apt-get autoclean

RUN mkdir /bot
COPY . /bot/
WORKDIR /bot

RUN pip install -U aiogram
RUN pip install psycopg2-binary

CMD ["python", "./main.py"]
