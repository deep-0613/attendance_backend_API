from flask import Blueprint, request, jsonify
from db import get_connection

fcm_bp = Blueprint('fcm', __name__)

@fcm_bp.route('/save-token', methods=['POST'])
def save_token():
    data = request.json

    faculty_id = data.get("faculty_id")
    token = data.get("token")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO fcm_tokens (faculty_id, token)
        VALUES (%s, %s)
        ON CONFLICT (faculty_id)
        DO UPDATE SET token = EXCLUDED.token,
                      updated_at = CURRENT_TIMESTAMP
    """, (faculty_id, token))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Token saved"})