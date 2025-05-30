from flask import jsonify
from app import create_app
from flask_limiter.errors import RateLimitExceeded
from sqlalchemy.orm.exc import NoResultFound

app = create_app()

@app.errorhandler(RateLimitExceeded)
def ratelimit_handler(e):
    return jsonify({
        "error": "Too many requests",
        "message": str(e.description),
    }), 429

@app.errorhandler(404)
def ratelimit_handler(e):
    return jsonify({
        "error": "Not Found",
        "message": "Not Found",
    }), 404

@app.errorhandler(Exception)
def handle_exception(e):
    response = {
        "error": str(e),
        "message": "An unexpected error occurred."
    }
    return jsonify(response), 500
    

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
