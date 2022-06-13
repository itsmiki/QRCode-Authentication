from flask import Flask, render_template
from flask import request
from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route("/")
def home():
    return render_template('index.html')
    


if __name__ == "__main__":
    app.run("127.0.0.1", 8080)