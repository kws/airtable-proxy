# Airtable Proxy

The Airtable Proxy is a simple Flask application that will make multiple paginated Airtable requests
on your behalf and return a single non-paginated result.

In many common tools, such as Excel and Power BI you will have to do scripting if you want to handle
Airtable paginated results. This proxy simplifies that process.

To achieve this result, the proxy will store your API key and data in memory for a short period of time.
Your API key might also show up in server logs as it sent in the query string. 
This is therefore not recommended for personal or sensitive data, unless you trust the proxy host.

You can simply launch this service yourself, and templates for Docker and Heroku are included.

## Deploying Docker Image

To run this code locally, you can pull and run the latest image with

```shell
docker run --rm -t -p5000:5000 kajws/airtable-proxy
```

The proxy should then be available on http://localhost:5000/ .

To build a version yourself, simply use the included [Dockerfile](./Dockerfile).

## Deploying to Heroku

You can also deploy for free to Heroku:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
