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
