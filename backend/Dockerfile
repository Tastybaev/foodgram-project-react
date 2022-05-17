FROM python:3.9.7-slim
WORKDIR /backend
COPY . .
RUN pip install -r requirements.txt
RUN pip install --upgrade pip
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0.0.0.0:8000"]