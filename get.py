import os
import requests
import pandas as pd
import re
from html import unescape
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
COOKIE = os.getenv("COOKIE")

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.5",
    "referer": "https://taboracademy.myschoolapp.com/lms-assignment/assignment-center/student?svcid=edu",
    "connection": "keep-alive",
    "cookie": COOKIE,
}

params = {
    "displayByDueDate": "true"
}

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = unescape(text)
    return re.sub(r"<.*?>", "", text).strip()

response = requests.get(API_URL, headers=headers, params=params, timeout=30)

print("Status:", response.status_code)
response.raise_for_status()

data = response.json()

# pandas shit
sections = [
    "DueToday",
    "DueTomorrow",
    "DueThisWeek",
    "DueNextWeek",
    "DueAfterNextWeek",
    "PastThisWeek",
    "PastLastWeek",
    "PastBeforeLastWeek",
]

rows = []
for section in sections:
    for item in data.get(section, []):
        rows.append({
            "Category": section,
            "Class": item.get("GroupName"),
            "Assignment": clean_text(item.get("ShortDescription")),
            "Due": item.get("DateDue"),
            "Type": item.get("AssignmentType"),
            "Points": item.get("MaxPoints"),
        })

df = pd.DataFrame(rows)

# Convert Due to datetime
df["Due"] = pd.to_datetime(df["Due"], errors="coerce")

# Sort by due date
df = df.sort_values(["Due", "Class"], na_position="last").reset_index(drop=True)

# Show a clean view!
print(df[["Category", "Class", "Assignment", "Due", "Points"]].to_string(index=False))
