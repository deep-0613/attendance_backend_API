from db import get_db_connection


def create_announcement_service(data):
    title = data.get("title")
    content = data.get("content")
    faculty_id = data.get("faculty_id")
    department = data.get("department")
    batch = data.get("batch")
    priority = data.get("priority", "Normal")  # Default to Normal if not provided

    # Validate required fields
    if not title or not content or not faculty_id or not department or not batch:
        return {"error": "Missing required fields: title, content, faculty_id, department, batch"}, 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert announcement
        cur.execute("""
            INSERT INTO announcements (title, content, faculty_id, department, batch, priority)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, created_at
        """, (title, content, faculty_id, department, batch, priority))

        result = cur.fetchone()
        announcement_id = result[0]
        created_at = result[1]

        conn.commit()
        cur.close()
        conn.close()

        return {
            "message": "Announcement created successfully",
            "announcement_id": announcement_id,
            "title": title,
            "content": content,
            "faculty_id": faculty_id,
            "department": department,
            "batch": batch,
            "priority": priority,
            "created_at": str(created_at)
        }, 201

    except Exception as e:
        return {"error": str(e)}, 500
