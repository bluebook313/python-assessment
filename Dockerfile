FROM python:3.12-slim
COPY . .
RUN pip install --no-index --find-links /requirements/ -r requirements.txt 
WORKDIR /app


EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]