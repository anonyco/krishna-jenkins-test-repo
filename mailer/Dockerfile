FROM python:3.10

WORKDIR /app/mailer
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY mailer.py .
COPY templates ./templates
CMD ["python","mailer.py"]

