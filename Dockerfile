FROM python:3.8

COPY requirements.txt .
COPY ./ ./

RUN pip3 install -r requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "myapp:app"]