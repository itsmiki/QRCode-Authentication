from codecs import unicode_escape_decode
from inspect import signature
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS
import string
import random
from threading import Timer
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

app = Flask(__name__)
CORS(app)

ACTIVE_CODES = {}

@app.route("/")
def home():
    x = {'id': 'Hello, World!'}
    return jsonify(ACTIVE_CODES)


@app.route("/getqrcode/v1/application/<app_id>", methods = ['GET'])
def get_qr(app_id):
    #print(request.json)
    print(app_id)

    def get_random_string():
        letters = string.ascii_uppercase
        result_str = ''.join(random.choice(letters) for i in range(12))
        ACTIVE_CODES[str(result_str)] = app_id
        timer = Timer(60.0, lambda: [ACTIVE_CODES.pop(result_str), print(result_str + "expired!")])
        timer.start()
        return(result_str)



    x = {'qrcode_key': get_random_string()}
    print(ACTIVE_CODES)

    return jsonify(x)

@app.route("/authorization/v1", methods=['POST'])
def check():
    username = request.form['username']
    qr_code = request.form['qr_code']
    signature = int(request.form['signature']).to_bytes(256, 'little')
    print(signature)
    #print(request.form)
    #print(signature)

    rsa_public_key = RSA.importKey(open("public_keys/" + username + ".pem", "rb").read())
    verifier = PKCS1_v1_5.new(rsa_public_key)

    hash = SHA256.new(bytes(qr_code, encoding='utf-8'))
    # #print(type(signature))
    decrypted = verifier.verify(hash, signature)
    print(decrypted)

    return jsonify(decrypted)

    # message = 

    # verifier = PKCS1_v1_5.new(rsa_key)
    # h = SHA.new(signed_qrcode)
    # if verifier.verify(h, signature_received_with_the_data):
    #     print "OK"
    # else:
    #     print "Invalid"
    
    
    return jsonify("Works!")
    


if __name__ == "__main__":

    app.run(debug=True)