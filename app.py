from flask import Flask
import redis
import mysql.connector

app = Flask(__name__)

# Connect to Redis
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# Connect to MySQL
def get_mysql_connection():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="flask_db"
    )

@app.route("/")
def home():
    redis_client.set("message", "Hello from Redis!")
    message = redis_client.get("message")

    return f"Flask + MySQL + Redis! Redis says: {message} 124"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
