FROM python:3.8-buster

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 80

COPY app.py app.py

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]