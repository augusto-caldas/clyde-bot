FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py discord_token.txt system_input.txt ./

CMD ["python", "main.py"]