import os, requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv(dotenv_path="/Users/jeffboerger/Dev/commission-calculator/.env")

session = requests.Session()
session.post(
    os.getenv("LOGIN_URL"),
    data={"login_username": os.getenv("SITE_USERNAME"), "login_password": os.getenv("SITE_PASSWORD")}
)

resp = session.get("https://freedomhoustonsouth.ourers.com/cp/review_events/2327/view-logs/")
soup = BeautifulSoup(resp.text, "html.parser")

for row in soup.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) >= 4:
        print([c.text.strip() for c in cells[:4]])
