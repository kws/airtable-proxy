import json
import os
from airtable import Airtable
from cryptography.fernet import Fernet
from flask import Flask, request, Response
from base64 import urlsafe_b64decode, urlsafe_b64encode

try:
    FERNET = Fernet(os.environ['SECRET_KEY'])
except:
    FERNET = Fernet(Fernet.generate_key())


def _opt_params_(*opts, args=None, kwargs=None):
    if kwargs is None:
        kwargs = dict()
    else:
        kwargs = dict(**kwargs)
    for arg in opts:
        value = args.get(arg)
        if value is not None:
            kwargs[arg] = value
    return kwargs


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return app.send_static_file('index.html')

    @app.route('/airtable/genkey')
    def genkey():
        if FERNET is None:
            return 'server not configured for encryption', 500

        params = _opt_params_("base_id", "table_name", "api_key", "view", "fields", "sort", "formula",
                              args=request.args)
        params['random'] = os.urandom(24).hex()
        auth_header = request.headers.get("Authorization")
        if auth_header is not None:
            params['api_key'] = auth_header.split(" ")[1]

        token = FERNET.encrypt(json.dumps(params).encode('utf-8'))
        return urlsafe_b64encode(token)

    @app.route('/airtable/download')
    def download_download():
        id = request.args.get('id')
        kwargs = _opt_params_("view", "fields", "sort", "formula", args=request.args)

        if id is not None and FERNET is None:
            return 'server not configured for encryption', 500

        elif id is not None:
            encrypted_data = urlsafe_b64decode(id)
            encrypted_data = FERNET.decrypt(encrypted_data)
            args = json.loads(encrypted_data)
            kwargs = _opt_params_("view", "fields", "sort", "formula", args=args, kwargs=kwargs)

        else:
            args = request.args

        base_id = args['base_id']
        table_name = args['table_name']
        api_key = args['api_key']

        airtable = Airtable(base_id, table_name, api_key)

        def generate():
            first_record = True
            for page in airtable.get_iter(**kwargs):
                for record in page:
                    if first_record:
                        yield "["
                        first_record = False
                    else:
                        yield ","
                    yield json.dumps(record)
            yield ']'
        return Response(generate(), mimetype="application/json")

    return app
