FROM python:3.9

# install chromedriver
RUN apt update
RUN apt install -y chromium

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install --no-cache-dir uvicorn gunicorn
COPY ./app /app
WORKDIR /

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

ENV PYTHONPATH=/app

CMD ["/start.sh"]
