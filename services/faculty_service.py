from db import get_db_connection


def get_faculty_batches_service(faculty_id):
    if not faculty_id:
        return {"error": "faculty_id parameter is required"}, 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Query to get distinct batches for the given faculty_id
        cur.execute("""
            SELECT DISTINCT batch, course_name, course_code
            FROM timetable
            WHERE faculty_id = %s
            ORDER BY batch
        """, (faculty_id,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        # Extract unique batches (using set to avoid duplicates)
        batches = set()
        for row in rows:
            batches.add(row[0])

        return {
            "faculty_id": faculty_id,
            "assigned_batches": list(batches)
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500


def get_student_count_service(batch):
    if not batch:
        return {"error": "batch parameter is required"}, 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Query to count students for the given batch/year
        cur.execute("""
            SELECT COUNT(roll_number)
            FROM students
            WHERE year = %s
        """, (batch,))

        result = cur.fetchone()
        student_count = result[0] if result else 0

        cur.close()
        conn.close()

        return {
            "batch": batch,
            "student_count": student_count
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500


def get_assigned_courses_service(faculty_id):
    if not faculty_id:
        return {"error": "faculty_id parameter is required"}, 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Query to get distinct batches, courses, lab batches, and session types for faculty
        cur.execute("""
            SELECT DISTINCT batch, course_name, lab_batch, session_type
            FROM timetable
            WHERE faculty_id = %s
            ORDER BY batch, course_name
        """, (faculty_id,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        result = []
        for r in rows:
            result.append({
                "batch": r[0],
                "course_name": r[1],
                "lab_batch": r[2],
                "session_type": r[3]
            })

        return result, 200

    except Exception as e:
        return {"error": str(e)}, 500
