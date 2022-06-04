FROM python:3.9.7-slim
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
COPY . /code
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0.0.0.0:8000"]