from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from flask_cors import CORS
from google import genai
from google.genai.types import GenerateContentConfig
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockSnapshotRequest


# Load environment variables from .env
load_dotenv()
GEM_API_KEY = os.getenv("GEMINI_API_KEY")
ALP_API_KEY = os.getenv("APCA_API_KEY_ID")
ALP_API_SECRET = os.getenv("APCA_API_SECRET_KEY")

# Initialize Google client
gem_client = genai.Client(api_key=GEM_API_KEY)
alp_client = StockHistoricalDataClient(ALP_API_KEY, ALP_API_SECRET)

# Flask app
app = Flask(__name__)
CORS(app)  # Allow everything for local dev

# Simulated user profile
user_profile = {
    "experience": "beginner",
    "risk_tolerance": "medium",
    "goals": "long-term growth"
}



@app.route("/tickers", methods=["GET"])
def get_ticker_data():
    symbols_param = request.args.get("symbols", "")
    symbols = [s.strip().upper() for s in symbols_param.split(",") if s.strip()]

    if not symbols:
        return jsonify({"error": "No symbols provided"}), 400

    try:
        snapshot_request = StockSnapshotRequest(symbol_or_symbols=symbols)
        snapshots = alp_client.get_stock_snapshot(snapshot_request)

        response = {}
        for symbol in symbols:
            snapshot = snapshots.get(symbol)
            if snapshot:
                current = snapshot.latest_trade.price
                prev_close = snapshot.previous_daily_bar.close
                change = current - prev_close
                percent = (change / prev_close) * 100 if prev_close else 0
                response[symbol] = {
                    "price": round(current, 2),
                    "change": round(change, 2),
                    "percent_change": round(percent, 2),
                    "direction": "up" if change > 0 else "down" if change < 0 else "unchanged"
                }
            else:
                response[symbol] = {"error": "Data not found"}

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
                "Be friendly, clear, and helpful. Oh, and don't use any markdown."
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

        response = gem_client.models.generate_content(
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
