# security_scan.py
from pathlib import Path

def check_security(path):
    text = Path(path).read_text().lower()
    if "password" not in text:
        return "no password check found"
    return None

if __name__ == "__main__":
    print(check_security("main.py"))