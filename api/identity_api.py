import flask_cors
from api import app


@app.route('/identity')
def identity_api():
    return "Identity tested!"
