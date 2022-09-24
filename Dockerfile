FROM python:3.8

COPY requirements.txt .
COPY ./ ./
COPY app.py .

RUN pip3 install -r requirements.txt
CMD ["python", "app.py"]