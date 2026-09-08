FROM python:3.14

WORKDIR /app

COPY app.py .

CMD ["python3", "app.py"]
