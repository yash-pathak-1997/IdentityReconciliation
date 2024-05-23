from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
cors = CORS(app)


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
