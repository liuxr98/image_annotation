FROM python:3.9-slim-buster

WORKDIR /home/app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .
EXPOSE 5000
#ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "annotate.wsgi:app"]