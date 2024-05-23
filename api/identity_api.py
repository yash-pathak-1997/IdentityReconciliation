from flask import request, jsonify, render_template
from flask_cors import cross_origin
from api import app


@app.route('/identity', methods=['GET', 'POST'])
@cross_origin()
def identity_api():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        phone_number = data.get('phoneNumber')

        response = {
            'message': 'Data received successfully',
            'email': email,
            'phoneNumber': phone_number
        }

        return jsonify(response)

    else:
        return render_template('identity_template.html')
