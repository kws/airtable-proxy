import json
import os
from airtable import Airtable
from flask import Flask, request, send_file, Response


def _opt_params_(*args):
    kwargs = dict()
    for arg in args:
        value = request.args.get(arg)
        if value is not None:
            kwargs[arg] = value
    return kwargs


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return app.send_static_file('index.html')

    @app.route('/airtable/download')
    def download_download():
        base_id = request.args.get('base_id')
        table_name = request.args.get('table_name')
        api_key = request.args.get('api_key')

        airtable = Airtable(base_id, table_name, api_key)

        kwargs = _opt_params_("view", "fields", "sort", "formula")

        def generate():
            print_sep = False
            yield '['
            for page in airtable.get_iter(**kwargs):
                for record in page:
                    if print_sep:
                        yield ","
                    else:
                        print_sep = True
                    yield json.dumps(record)
            yield ']'
        return Response(generate(), mimetype="application/json")

    return app
