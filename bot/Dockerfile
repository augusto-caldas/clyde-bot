FROM python:3.12-slim

WORKDIR /app
COPY main.py requirements.txt tokens.txt ./
RUN pip install requirements.txt

CMD ["python", "main.py"]