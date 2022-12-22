import uuid
import json
import base64

def createQRCodeData_base64(action):
    qr_content = {}
    qr_content['action'] = action
    qr_content['token'] = str(uuid.uuid4())
    qr = json.dumps(qr_content)
    encoded = base64.b64encode(str(qr).encode('utf-8')).decode('utf-8')
    return encoded

def createQRCodeData_dict(action):
    qr_content = {}
    qr_content['action'] = action
    qr_content['token'] = str(uuid.uuid4())
    return qr_content