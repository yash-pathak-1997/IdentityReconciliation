from flask import request, jsonify, render_template
from flask_cors import cross_origin
from api import app
from model import IdentityRequestModel
from service import identity_service


@app.route('/identity', methods=['GET', 'POST'])
@cross_origin()
def identity_api():
    if request.method == 'POST':
        data = request.get_json()
        identity_request = IdentityRequestModel(email=data['email'], phoneNumber=data['phoneNumber'])
        response = identity_service(identity_request)
        return jsonify(response)

    else:
        return render_template('identity_template.html')
