FROM python:3.8

COPY requirements.txt .
COPY ./ ./

RUN pip3 install -r requirements.txt
CMD ["python", "myapp.py"]