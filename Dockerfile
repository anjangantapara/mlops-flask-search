FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN pip install -e .
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0"]