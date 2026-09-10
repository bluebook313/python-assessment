FROM python:3.12-slim
WORKDIR /app

COPY . .

RUN pip install --no-index --find-links requirements/ -r requirements.txt 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]