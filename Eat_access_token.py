import requests
import urllib3
import os
import time
import sys
from urllib.parse import urlparse, parse_qs, unquote

urllib3.disable_warnings()

# ==============================
# COLORS
# ==============================

R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
C = "\033[96m"
W = "\033[0m"
B = "\033[1m"

# ==============================
# CLEAR SCREEN
# ==============================

def clear():
    os.system("clear")

# ==============================
# LOADING
# ==============================

def loading(text="Processing"):
    spinner = ["|", "/", "-", "\\"]
    for i in range(30):
        sys.stdout.write(f"\r{C}⏳ {text} {spinner[i % 4]}{W}")
        sys.stdout.flush()
        time.sleep(0.07)
    print("\r", end="")

# ==============================
# BANNER
# ==============================

def banner():
    print(C + B + """
╔══════════════════════════════════════╗
║        🔥 EAT TOKEN CLI TOOL 🔥      ║
║          Fast & Clean Mode           ║
╚══════════════════════════════════════╝
""" + W)

# ==============================
# FUNCTIONS
# ==============================

def extract_eat(user_input):
    if "http" in user_input:
        parsed = urlparse(user_input)
        params = parse_qs(parsed.query)
        return params.get("eat", [None])[0]
    return user_input.strip()

def get_access_token(eat):
    try:
        url = f"https://api-otrss.garena.com/support/callback/?access_token={eat}"
        r = requests.get(url, allow_redirects=True, timeout=10)
        final = parse_qs(urlparse(r.url).query)
        return final.get("access_token", [None])[0]
    except:
        return None

def get_uid(access_token):
    try:
        url = "https://prod-api.reward.ff.garena.com/redemption/api/auth/inspect_token/"
        headers = {"access-token": access_token}
        r = requests.get(url, headers=headers, verify=False, timeout=10)
        data = r.json()
        return data.get("uid"), data.get("region")
    except:
        return None, None

def extract_info_from_url(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    uid = params.get("account_id", ["Unknown"])[0]
    region = params.get("region", ["Unknown"])[0]
    name = params.get("nickname", ["Unknown"])[0]

    return uid, region, unquote(name)

# ==============================
# MAIN
# ==============================

clear()

print(Y + "\n👉 Enter EAT Token / URL:\n" + W)
eat_input = input(C + "➤ " + W)

print()
loading("Fetching Data")

eat = extract_eat(eat_input)

if not eat:
    print(R + "\n❌ Invalid EAT Token!" + W)
    exit()

access_token = get_access_token(eat)

# fallback URL
uid_url, region_url, name_url = extract_info_from_url(eat_input)

uid_api, region_api = None, None
if access_token:
    uid_api, region_api = get_uid(access_token)

# final values
uid = uid_api if uid_api else uid_url
region = region_api if region_api else region_url
name = name_url

# ==============================
# OUTPUT
# ==============================

clear()
banner()

print(G + "\n✅ RESULT\n" + W)

print(C + "╔══════════════════════════════════════╗" + W)

print(f"{B}│ 🔑 Access Token : {G}{access_token or 'Failed'}{W}")
print(f"{B}│ 👤 Name         : {C}{name}{W}")
print(f"{B}│ 🆔 UID          : {Y}{uid}{W}")
print(f"{B}│ 🌍 Region       : {R}{region}{W}")

print(C + "╚══════════════════════════════════════╝" + W)

print(C + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + W)
print(G + "✨ Data fetched successfully!\n" + W)