FROM python:3.7

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY . /app
WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 8080 

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]
