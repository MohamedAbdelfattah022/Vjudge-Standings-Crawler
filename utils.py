import os
from dotenv import load_dotenv
import json

load_dotenv()

def login(session, login_url, headers):
    payload = {
        'username': os.getenv("user"),
        'password': os.getenv("password")
    }
    
    response = session.post(login_url, data=payload, headers=headers)
    if response.ok:
        print("Login successful!")
        return True
    else:
        print("Login failed.")
        return False

def fetch_standings(session, contest_url, headers):
    response = session.get(contest_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch standings:", response.status_code)
        return None

def unify_data(standings):
    unified_data = {}
    
    for participant_id, info in standings["participants"].items():
        unified_data[participant_id] = {
            "handle": info[0],
            "display_name": info[1],
            "submissions": [],
        }
    
    for submission in standings['submissions']:
        participant_id = str(submission[0])
        problem_index = submission[1]
        status = submission[2]
        
        submission_entry = {
            "problem_index": problem_index,
            "status": status,
        }
        
        if participant_id not in unified_data:
            unified_data[participant_id]["submissions"] = [submission_entry]
        else:
            unified_data[participant_id]["submissions"].append(submission_entry)
    
    return unified_data

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
