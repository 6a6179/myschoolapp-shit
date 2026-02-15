import os
import requests
import pandas as pd
import re
from html import unescape
from dotenv import load_dotenv

load_dotenv()

SUBDOMAIN = os.getenv("SCHOOL_SUBDOMAIN")
API_URL = f"https://{SUBDOMAIN}.myschoolapp.com/api/assignment2/StudentAssignmentCenterGet"

try:
    with open("cookie.txt", "r") as f:
        COOKIE = f.read().strip()
except FileNotFoundError:
    print("Error: cookie.txt not found. Run auth.py first.")
    exit(1)

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.5",
    "referer": f"https://{SUBDOMAIN}.myschoolapp.com/lms-assignment/assignment-center/student",
    "connection": "keep-alive",
    "cookie": COOKIE,
}

params = {"displayByDueDate": "true"}


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = str(text)
    text = unescape(text)
    return re.sub(r"<.*?>", "", text).strip()


STATUS_MAP = {
    1: "Completed",
    0: "In progress",
    2: "Overdue",
    -2147483648: "To do",
}


def status_label(code) -> str:
    try:
        code_int = int(code)
    except (TypeError, ValueError):
        return "Unknown"
    return STATUS_MAP.get(code_int, f"Unknown ({code_int})")


try:
    response = requests.get(API_URL, headers=headers, params=params, timeout=30)
    print("Status:", response.status_code)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    print(f"Error: {e}")
    exit(1)

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
        code = item.get("StudentStatus")
        
        rows.append({
            "Category": section,
            "Class": item.get("GroupName"),
            "Assignment": clean_text(item.get("ShortDescription")),
            "Due": item.get("DateDue"),
            "Type": item.get("AssignmentType"),
            "Points": item.get("MaxPoints"),
            "StudentStatusCode": code,
            "StudentStatus": status_label(code),
        })

if not rows:
    print("No assignments found.")
    exit()

df = pd.DataFrame(rows)

df["Due"] = pd.to_datetime(df["Due"], errors="coerce")

STATUS_ORDER = {"Overdue": 0, "To do": 1, "In progress": 2, "Completed": 3}
df["StatusRank"] = df["StudentStatus"].map(STATUS_ORDER).fillna(99).astype(int)

df = df.sort_values(["StatusRank", "Due", "Class"], na_position="last").reset_index(drop=True)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

print(df[["Category", "StudentStatus", "Class", "Assignment", "Due", "Points"]].to_string(index=False))