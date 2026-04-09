import firebase_admin
from firebase_admin import credentials, messaging
from db import get_db_connection

# Initialize once
cred = credentials.Certificate("final-year-project-ecbf3-firebase-adminsdk-fbsvc-b8434f6229.json")
firebase_admin.initialize_app(cred)

def send_fcm_to_multiple(tokens, title, body):
    success_count = 0
    failure_count = 0
    
    for token in tokens:
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                token=token,
            )
            
            messaging.send(message)
            success_count += 1
            print(f"Successfully sent to token: {token}")
        except Exception as e:
            failure_count += 1
            print(f"Failed to send to token {token}: {e}")
    
    print("Success:", success_count)
    print("Failure:", failure_count)

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