from flask import Flask, jsonify
from flask import request
from flask_cors import CORS
import string
import random

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    x = {'id': 'Hello, World!'}
    return jsonify(x)


@app.route("/getqrcode/v1/application/<app_id>", methods = ['GET'])
def get_qr(app_id):
    #print(request.json)
    print(app_id)

    def get_random_string():
        letters = string.ascii_uppercase
        result_str = ''.join(random.choice(letters) for i in range(12))
        return(result_str)

    x = {'qrcode_key': get_random_string()}
    return jsonify(x)

@app.route("/")
def check():
    pass
    


if __name__ == "__main__":
    app.run(debug=True)