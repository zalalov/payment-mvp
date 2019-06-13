FROM python:3

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && python manage.py db upgrade && python run.py
