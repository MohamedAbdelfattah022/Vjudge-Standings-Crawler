import requests
from utils import login, fetch_standings, unify_data, save_to_json

def main():
    session = requests.Session()
    
    contest_id = "665213"
    login_url = "https://vjudge.net/user/login"
    contest_url = f"https://vjudge.net/contest/rank/single/{contest_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    if not login(session, login_url, headers):
        print("Login failed. Exiting.")
        return

    standings = fetch_standings(session, contest_url, headers)
    if standings is None:
        return

    unified_data = unify_data(standings)

    save_to_json(unified_data, f'{contest_id}unified_data.json')

if __name__ == "__main__":
    main()
