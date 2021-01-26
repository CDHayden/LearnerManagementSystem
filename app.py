import os
from lms import app

if __name__ == "__main__":
    host = os.environ.get("HOST","127.0.0.1")
    port = os.environ.get("PORT","5050")

    app.run(host, port)
