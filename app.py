import os
import jsonstreams
import tempfile
from airtable import Airtable
from flask import Flask, request, send_file


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

        with tempfile.NamedTemporaryFile(mode="wt", delete=False) as FILE:
            try:
                with jsonstreams.Stream(jsonstreams.Type.object, fd=FILE) as STREAM:
                    with STREAM.subarray('records') as records:
                        for page in airtable.get_iter(**kwargs):
                            for record in page:
                                records.write(record)

                return send_file(FILE.name, attachment_filename=f"{table_name}.json")
            finally:
                os.unlink(FILE.name)

    return app
