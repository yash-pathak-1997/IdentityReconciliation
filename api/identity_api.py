from flask_cors import cross_origin
from api import app


@app.route('/identity')
@cross_origin()
def identity_api():
    return "Identity tested!"
