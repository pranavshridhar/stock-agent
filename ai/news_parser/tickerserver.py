from flask import Flask, request, jsonify
from flask_cors import CORS
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockSnapshotRequest
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("APCA_API_KEY_ID")
API_SECRET = os.getenv("APCA_API_SECRET_KEY")

client = StockHistoricalDataClient(API_KEY, API_SECRET)

app = Flask(__name__)
CORS(app)  # Allow CORS for all origins

@app.route("/tickers", methods=["GET"])
def get_ticker_data():
    symbols_param = request.args.get("symbols", "")
    symbols = [s.strip().upper() for s in symbols_param.split(",") if s.strip()]

    if not symbols:
        return jsonify({"error": "No symbols provided"}), 400

    try:
        snapshot_request = StockSnapshotRequest(symbol_or_symbols=symbols)
        snapshots = client.get_stock_snapshot(snapshot_request)

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

if __name__ == "__main__":
    app.run(debug=True)
