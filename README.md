# Airtable Proxy

The Airtable Proxy is a simple Flask application that will make multiple paginated Airtable requests
on your behalf and return a single non-paginated result.

In many common tools, such as Excel and Power BI you will have to do scripting if you want to handle
Airtable paginated results. This proxy simplifies that process.

To achieve this result, the proxy will temporarily store your results on disk. This is therefore not
recommended for personal or sensitive data, unless you trust the proxy host.

You can simply launch this service yourself, and templates for Docker and Heroku are included.

