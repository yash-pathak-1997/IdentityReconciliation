import os
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Load environment variables from .env file
load_dotenv()

# template folder path relative to this file's location
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'template'))

app = Flask(__name__, template_folder=template_dir)
api = Api(app)
CORS(app)

# SQLAlchemy setup
db_string = os.getenv('DB_CONN_STRING')
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
db = SQLAlchemy(app)
db.init_app(app)


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
