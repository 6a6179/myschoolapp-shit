# myschoolapp-shit

## Authentication limitations

- This project currently supports Microsoft OAuth 2.0 login flow only.
- Accounts with 2FA/MFA enabled are not supported by `auth.py` and login may fail.

## Run locally (Windows PowerShell)

1. Clone the repository and enter the project folder:
```powershell
git clone https://github.com/6a6179/myschoolapp-shit.git
cd myschoolapp-shit
```

2. Create and activate a virtual environment (you can ignore this if your IDE automatically creates the virtual environment):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
python -m playwright install chromium
```

4. Create `.env` in the project root (look at .env.example for more details):
```env
SCHOOL_SUBDOMAIN=your-school-subdomain
SCHOOL_EMAIL=your-email@example.com
SCHOOL_PASS=your-password
HEADLESS=False
TIMEOUT=30000
```

5. Generate a fresh login cookie:
```powershell
python auth.py
```

6. Fetch assignments:
```powershell
python get.py
```

## Run locally (macOS/Linux)

1. Clone the repository and enter the project folder:
```bash
git clone https://github.com/6a6179/myschoolapp-shit.git
cd myschoolapp-shit
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
python -m playwright install chromium
```

4. Create `.env` in the project root:
```env
SCHOOL_SUBDOMAIN=your-school-subdomain
SCHOOL_EMAIL=your-email@example.com
SCHOOL_PASS=your-password
HEADLESS=False
TIMEOUT=30000
```

5. Generate a fresh login cookie:
```bash
python auth.py
```

6. Fetch assignments:
```bash
python get.py
```

## Notes

- `auth.py` creates `cookie.txt` after a successful login.
- If `cookie.txt` is missing or expired, run `python auth.py` again.
