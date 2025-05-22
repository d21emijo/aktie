from flask import Flask, render_template, jsonify,request,redirect
from models import db, PredictionResult
from routes.prediction import procenten
from flask_cors import CORS

app = Flask(__name__,template_folder="templates")
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///results.db"
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    results = PredictionResult.query.order_by(PredictionResult.created_at.desc()).limit(5).all()
    return render_template("html.html", results=results)


@app.route("/last_prediction", methods=["GET"])
def last_predictions():
    try:
        results = PredictionResult.query.order_by(PredictionResult.created_at.desc()).limit(5).all()
        predictions = [
            {
                "ticker": r.ticker,
                "accuracy": r.accuracy,
                "time": r.created_at.isoformat()
            }
            for r in results
        ]
        return jsonify({"predictions": predictions})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        ticker = data.get("ticker", "AAPL").upper()
        print("ticker",ticker)
        procenten(ticker)  

        return jsonify({"status": "success", "ticker": ticker})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)