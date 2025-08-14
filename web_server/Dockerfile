FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install cryptography
COPY . .
EXPOSE 80
CMD ["python", "app.py"]

