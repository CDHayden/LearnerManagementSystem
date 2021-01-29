from os import environ
from lms import create_app

if __name__ == "__main__":
    app = create_app()
    host = environ.get("HOST", "0.0.0.0")
    port = environ.get("PORT", "5000")
    app.run(host, port)
