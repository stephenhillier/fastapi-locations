FROM python:3.7

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 8000 

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["uvicorn", "main:app", "--reload", "--debug", "--host", "0.0.0.0"]
