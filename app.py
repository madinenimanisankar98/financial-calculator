"""
Financial Calculator PRO — Flask application.
Run locally with:  python app.py
"""

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from backend.calculations import (
    calculate_savings,
    calculate_emi,
    calculate_gst,
    calculate_percentage,
)
from backend.learn_data import get_learn_content
from backend.ai_helper import answer_question

load_dotenv()

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Page route
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------------------------------------------------------
# Calculator APIs
# ---------------------------------------------------------------------------

@app.route("/api/savings", methods=["POST"])
def api_savings():
    data = request.get_json(force=True) or {}
    try:
        result = calculate_savings(
            monthly_income=float(data["monthly_income"]),
            monthly_expenses=float(data["monthly_expenses"]),
            goal_name=data.get("goal_name", "Your goal"),
            goal_price=float(data["goal_price"]),
            target_value=float(data["target_value"]) if data.get("target_value") else None,
            target_unit=data.get("target_unit"),
        )
        return jsonify(result)
    except (KeyError, ValueError, TypeError) as exc:
        return jsonify({"error": f"Invalid input: {exc}"}), 400


@app.route("/api/emi", methods=["POST"])
def api_emi():
    data = request.get_json(force=True) or {}
    try:
        result = calculate_emi(
            principal=float(data["principal"]),
            annual_rate=float(data["annual_rate"]),
            tenure_value=float(data["tenure_value"]),
            tenure_unit=data.get("tenure_unit", "years"),
            emis_paid=int(data.get("emis_paid", 0) or 0),
        )
        return jsonify(result)
    except (KeyError, ValueError, TypeError, ZeroDivisionError) as exc:
        return jsonify({"error": f"Invalid input: {exc}"}), 400


@app.route("/api/gst", methods=["POST"])
def api_gst():
    data = request.get_json(force=True) or {}
    try:
        result = calculate_gst(
            price=float(data["price"]),
            gst_percent=float(data["gst_percent"]),
            tax_mode=data.get("tax_mode", "exclusive"),
            product_name=data.get("product_name"),
        )
        return jsonify(result)
    except (KeyError, ValueError, TypeError) as exc:
        return jsonify({"error": f"Invalid input: {exc}"}), 400


@app.route("/api/percentage", methods=["POST"])
def api_percentage():
    data = request.get_json(force=True) or {}
    try:
        result = calculate_percentage(
            total=float(data["total"]),
            percentage=float(data["percentage"]),
        )
        return jsonify(result)
    except (KeyError, ValueError, TypeError) as exc:
        return jsonify({"error": f"Invalid input: {exc}"}), 400


# ---------------------------------------------------------------------------
# Learn + AI assistant APIs
# ---------------------------------------------------------------------------

@app.route("/api/learn")
def api_learn():
    lang = request.args.get("lang", "en")
    return jsonify(get_learn_content(lang))


@app.route("/api/ask-ai", methods=["POST"])
def api_ask_ai():
    data = request.get_json(force=True) or {}
    question = data.get("question", "")
    return jsonify(answer_question(question))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
