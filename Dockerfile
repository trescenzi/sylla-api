FROM python:3-slim

WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python", "app.py"]
