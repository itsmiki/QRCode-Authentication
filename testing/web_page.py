from flask import Flask, render_template, redirect, url_for
from flask import request
from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        print(request.form['action'])
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)
    


if __name__ == "__main__":
    app.run("127.0.0.1", 8080, debug=True)