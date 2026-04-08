from google.cloud import firestore
import datetime

# Database init
db = firestore.Client(project="sprout-ai-492515")

def add_baby_task(time: str, activity: str, description: str = "No description"):
    try:
        doc_ref = db.collection('sprout_tasks').document()
        doc_ref.set({
            'time': str(time),
            'activity': str(activity),
            'description': str(description),
            'status': 'scheduled',
            'created_at': datetime.datetime.now()
        })
        return f"Done! Scheduled {activity} for {time}."
    except Exception as e:
        return f"DB Error: {str(e)}"

def get_today_plan():
    try:
        docs = db.collection("sprout_tasks").stream()
        plan = [f"[{d.to_dict().get('time')}] {d.to_dict().get('activity')}" for d in docs]
        return " | ".join(plan) if plan else "Empty Schedule."
    except Exception as e:
        return f"Fetch Error: {str(e)}"

def clear_all_tasks():
    try:
        docs = db.collection("sprout_tasks").stream()
        for d in docs:
            d.reference.delete()
        return "Success: Database cleared."
    except Exception as e:
        return f"Clear Error: {str(e)}"