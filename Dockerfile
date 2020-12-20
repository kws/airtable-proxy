FROM python:3.9-alpine

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY static static
COPY templates templates
COPY app.py app.py

ENV HOST=0.0.0.0 PORT=5000

EXPOSE $PORT

CMD waitress-serve --host "$HOST" --port "$PORT" --call app:create_app