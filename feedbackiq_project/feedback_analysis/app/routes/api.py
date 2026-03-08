"""
app/routes/api.py
REST API endpoints for feedback analysis
"""

import os
import json
import traceback
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from app.modules.preprocessor import TextPreprocessor
from app.modules.sentiment import SentimentAnalyzer
from app.modules.theme_extractor import ThemeExtractor
from app.modules.insight_generator import InsightGenerator
from app.modules.visualizer import Visualizer

api_bp = Blueprint("api", __name__)

# ── helpers ────────────────────────────────────────────────────────────────────

def allowed_file(filename: str) -> bool:
    allowed = current_app.config.get("ALLOWED_EXTENSIONS", {"csv", "txt", "json"})
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


def _run_pipeline(feedback_list: list[str]) -> dict:
    """Run the full NLP pipeline on a list of feedback strings."""
    preprocessor = TextPreprocessor()
    sentiment_analyzer = SentimentAnalyzer()
    theme_extractor = ThemeExtractor()
    insight_generator = InsightGenerator()
    visualizer = Visualizer()

    # 1. Preprocess
    cleaned = preprocessor.process_batch(feedback_list)

    # 2. Sentiment analysis
    sentiments = sentiment_analyzer.analyze_batch(feedback_list)

    # 3. Theme extraction
    themes = theme_extractor.extract(cleaned)

    # 4. Insights
    insights = insight_generator.generate(sentiments, themes, feedback_list)

    # 5. Charts (base64 encoded)
    charts = visualizer.generate_all(sentiments, themes)

    return {
        "total_feedback": len(feedback_list),
        "sentiments": sentiments,
        "themes": themes,
        "insights": insights,
        "charts": charts,
    }


# ── endpoints ──────────────────────────────────────────────────────────────────

@api_bp.route("/analyze/text", methods=["POST"])
def analyze_text():
    """
    Analyze raw feedback text submitted as JSON.
    Body: { "feedback": ["text1", "text2", ...] }
    """
    data = request.get_json(silent=True)
    if not data or "feedback" not in data:
        return jsonify({"error": "Provide a JSON body with a 'feedback' list."}), 400

    feedback_list = data["feedback"]
    if not isinstance(feedback_list, list) or len(feedback_list) == 0:
        return jsonify({"error": "'feedback' must be a non-empty list of strings."}), 400

    try:
        result = _run_pipeline(feedback_list)
        return jsonify(result), 200
    except Exception as exc:
        traceback.print_exc()
        return jsonify({"error": str(exc)}), 500


@api_bp.route("/analyze/file", methods=["POST"])
def analyze_file():
    """
    Analyze feedback uploaded as a CSV / TXT / JSON file.
    For CSV: first column is used.
    For TXT:  one feedback item per line.
    For JSON: expects a list of strings or list of objects with a 'text' key.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed. Use CSV, TXT, or JSON."}), 400

    filename = secure_filename(file.filename)
    upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(upload_path)

    try:
        ext = filename.rsplit(".", 1)[1].lower()
        feedback_list = _parse_file(upload_path, ext)

        if not feedback_list:
            return jsonify({"error": "No feedback found in the uploaded file."}), 400

        result = _run_pipeline(feedback_list)
        return jsonify(result), 200

    except Exception as exc:
        traceback.print_exc()
        return jsonify({"error": str(exc)}), 500


def _parse_file(path: str, ext: str) -> list[str]:
    """Parse uploaded file into a list of feedback strings."""
    if ext == "txt":
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    if ext == "json":
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        if isinstance(raw, list):
            return [
                item if isinstance(item, str) else item.get("text", "")
                for item in raw
                if item
            ]
        raise ValueError("JSON file must contain a list.")

    if ext == "csv":
        import csv
        items = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if row:
                    items.append(row[0].strip())
        return items

    raise ValueError(f"Unsupported extension: {ext}")


@api_bp.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "message": "Feedback Analysis API is running."}), 200
