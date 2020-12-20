FROM python:3.9-alpine
RUN apk --update-cache add libressl

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN apk add --virtual build-dependencies build-base libressl-dev libffi-dev \
  && pip install -r requirements.txt \
  && apk del build-dependencies

COPY static static
COPY app.py app.py

ENV HOST=0.0.0.0 PORT=5000

EXPOSE $PORT

CMD waitress-serve --host "$HOST" --port "$PORT" --call app:create_app