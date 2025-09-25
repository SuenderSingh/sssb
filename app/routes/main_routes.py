from flask import Blueprint, jsonify

main_bp = Blueprint("main_bp", __name__)

@main_bp.route("/")
def home():
    return jsonify({"message": "Backend is running ✅"}), 200

@main_bp.route("/health")
def health():
    return jsonify({"status": "ok"}), 200
