FROM python:3.12-slim
WORKDIR /app
COPY frontend/telegram/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY frontend/telegram/ frontend/telegram/
CMD ["python", "-m", "frontend.telegram.bot.main"]
