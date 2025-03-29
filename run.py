from flask import jsonify
from app import create_app

app = create_app()


# @app.errorhandler(Exception)
# def handle_exception(e):
#     response = {
#         "error": str(e),
#         "message": "An unexpected error occurred."
#     }
#     return jsonify(response), 500
    

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
