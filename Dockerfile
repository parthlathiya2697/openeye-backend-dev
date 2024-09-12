# syntax=docker/dockerfile:1
FROM python:3.8

EXPOSE 8000

COPY . .

RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
WORKDIR /app
RUN cd /app

CMD ["python", "main.py"]
