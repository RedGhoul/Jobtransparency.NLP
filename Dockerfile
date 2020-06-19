FROM python:3.7.7-buster
WORKDIR /app
# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN python -m nltk.downloader all

COPY . /app
ENV FLASK_APP=app.py
EXPOSE 8080

CMD [ "gunicorn","-c","gunicorn.conf.py","app:app" ]
