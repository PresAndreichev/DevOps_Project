"""
This module contains the Flask application setup and the main route.
"""

import socket
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    """
    Returns a greeting message with the hostname of the server.
    """
    return f"Hello! I am a Flask application running on {socket.gethostname()}"

if __name__ == '__main__':
    # Note the extra host argument. If we didn't have it, our Flask app
    # would only respond to requests from inside our container
    app.run(host='0.0.0.0')
