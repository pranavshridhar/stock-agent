from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from flask_cors import CORS
from google import genai
from google.genai.types import GenerateContentConfig

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Google client
client = genai.Client(api_key=API_KEY)

# Flask app
app = Flask(__name__)
CORS(app)  # Allow everything for local dev

# Simulated user profile
user_profile = {
    "experience": "beginner",
    "risk_tolerance": "medium",
    "goals": "long-term growth"
}

@app.route("/chat", methods=["POST"])
def chat_with_model():
    data = request.get_json()
    history = data.get("history", [])

    if not history or not isinstance(history, list):
        return jsonify({"error": "Invalid or missing 'history'"}), 400

    try:
        config = GenerateContentConfig(
            system_instruction=[
                "You are an AI investment coach.",
                f"The user is a {user_profile['experience']} investor with {user_profile['risk_tolerance']} risk tolerance and is aiming for {user_profile['goals']}.",
                "Be friendly, clear, and helpful."
            ]
        )

        # ✅ Fix: parts must be dicts with {text: ...}
        contents = [
            {
                "role": msg["role"],
                "parts": [{"text": part} for part in msg["parts"]]
            }
            for msg in history
        ]

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=config
        )

        return jsonify({"response": response.text})

    except Exception as e:
        print("❌ Error from Gemini:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
