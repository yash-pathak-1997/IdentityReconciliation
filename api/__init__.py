import os

from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'template'))

app = Flask(__name__, template_folder=template_dir)
api = Api(app)
CORS(app)

db_string = os.getenv('DB_CONN_STRING')


# Mapping HomePage resource to homepage '/'
class HomePage(Resource):

    @staticmethod
    def get():
        return "Hello! How are you doing? Please add /identity to the URL to view results."

    @staticmethod
    def post():
        return "Hello! How are you doing? Please add /identity to the URL to view results."


api.add_resource(HomePage, '/')

# Importing all APIs
from api.identity_api import identity_api
