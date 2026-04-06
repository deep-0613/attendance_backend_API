from flask import Blueprint, request, jsonify
from db import get_db_connection
from services.fcm_service import (
    get_tokens_for_faculty_list,
    send_fcm_to_multiple
)

substitution_bp = Blueprint('substitution', __name__)

@substitution_bp.route('/substitution/request', methods=['POST'])
def request_substitution():
    data = request.json

    timetable_id = data.get('timetable_id')
    original_faculty = data.get('original_faculty_id')
    date = data.get('date')

    conn = get_db_connection()
    cur = conn.cursor()

    # 1. Create substitution
    cur.execute("""
    INSERT INTO lecture_substitutions
    (timetable_id, original_faculty_id, original_faculty_name, date)
    SELECT %s, f.faculty_id, f.name, %s
    FROM faculty f
    WHERE f.faculty_id = %s
    RETURNING id
    """, (timetable_id, date, original_faculty))

    substitution_id = cur.fetchone()[0]

    # 2. Get eligible faculty (same batch logic)
    cur.execute("""
        SELECT faculty_id FROM faculty
        WHERE faculty_id != %s
    """, (original_faculty,))

    faculty_list = [row[0] for row in cur.fetchall()]

    conn.commit()
    cur.close()
    conn.close()

    # 3. Get tokens
    tokens = get_tokens_for_faculty_list(faculty_list)

    # 4. Send FCM
    if tokens:
        send_fcm_to_multiple(
            tokens,
            "Lecture Substitution Request",
            f"Faculty {original_faculty} needs a substitute"
        )

    return jsonify({
        "message": "Substitution request sent",
        "substitution_id": substitution_id
    })

@substitution_bp.route('/substitution/respond', methods=['POST'])
def respond_substitution():
    data = request.json

    substitution_id = data.get('substitution_id')
    faculty_id = data.get('faculty_id')
    action = data.get('action')  # ACCEPT / REJECT

    conn = get_db_connection()
    cur = conn.cursor()

    if action == "ACCEPT":
        cur.execute("""
        UPDATE lecture_substitutions
        SET 
            substitute_faculty_id = f.faculty_id,
            substitute_faculty_name = f.name,
            status = 'ACCEPTED'
        FROM faculty f
        WHERE f.faculty_id = %s
        AND lecture_substitutions.id = %s
        AND lecture_substitutions.status = 'PENDING'
        """, (faculty_id, substitution_id))

        if cur.rowcount == 0:
            return jsonify({"message": "Already taken"}), 400

    elif action == "REJECT":
        # optional logic
        pass

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Response recorded"})