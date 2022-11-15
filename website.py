from website import create_app
from functions._jwt import getJWTPayload

app = create_app()

if __name__ == '__main__':
    app.run("0.0.0.0", port=8000, debug=True)
