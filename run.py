import os
from app import create_app
from flask import jsonify

app = create_app()

@app.route('/')  # Root path
def home():
    return jsonify({"message": "Welcome to the BasiGo API!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
