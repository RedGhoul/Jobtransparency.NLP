FROM python:3.7.7-buster

# We copy just the requirements.txt first to leverage Docker cache

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN pip install gunicorn

ENV FLASK_APP=app.py
EXPOSE 8080

CMD [ "gunicorn","-c","gunicorn.conf.py","app:app" ]