FROM ubuntu:latest
LABEL authors="yumi"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt
<<<<<<< HEAD
COPY . .
EXPOSE 8000
CMD python -m uvicorn main:app --reload
=======

COPY . .

EXPOSE 8000
CMD python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
>>>>>>> 9e3595f (added bot)
