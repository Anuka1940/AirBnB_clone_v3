#!/usr/bin/python3
"""Create the Flask application and register blueprints"""
import os
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(error):
    """Close the storage session."""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """Return json object for 404 not found errorr"""
    return jsonify({
                    "error": "Not found"
                    }), 404

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.environ.get("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
