#!/usr/bin/python3

"""
Flask App that integrates with AirBnB static HTML Template
"""

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, make_response
import os


app = Flask(__name__)

app.url_map.strict_slashes = False

# flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """
    this method calls .close()
    the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(Exception)
def global_error_handler(err):
    """
    Global Route to handle All Error Status Codes
    """
    if err.code is 404:
        err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)


if __name__ == '__main__':
    """
    MAIN Flask App
    """
    app.run(host=host, port=port, threaded=True)
