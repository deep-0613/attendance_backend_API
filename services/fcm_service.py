import firebase_admin
from firebase_admin import credentials, messaging
from db import get_db_connection

# Initialize once
cred = credentials.Certificate("final-year-project-ecbf3-firebase-adminsdk-fbsvc-0a94ad6a42.json")
firebase_admin.initialize_app(cred)

def send_fcm_to_multiple(tokens, title, body):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        tokens=tokens,
    )

    response = messaging.send_multicast(message)
    print("Success:", response.success_count)
    print("Failure:", response.failure_count)

def get_tokens_for_faculty_list(faculty_ids):
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT token FROM fcm_tokens
        WHERE faculty_id = ANY(%s)
    """

    cur.execute(query, (faculty_ids,))
    tokens = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    return tokens