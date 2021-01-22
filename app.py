import os
from lms import app

if __name__ == "__main__":
    host = os.environ["HOST"]
    port = os.environ["PORT"]

    app.run(host, port)
