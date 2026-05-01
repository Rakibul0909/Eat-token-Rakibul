import requests
import urllib.parse

def eat_to_access_token():
    print("\n=== EAT TO ACCESS TOKEN ===\n")

    user_input = input("Enter EAT Token OR Full EAT URL: ").strip()

    # 🔍 Extract EAT token
    eat_token = None
    if "http" in user_input:
        parsed_url = urllib.parse.urlparse(user_input)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        eat_token = query_params.get('eat', [None])[0]
    else:
        eat_token = user_input

    if not eat_token:
        print("\n[!] Invalid input! EAT token nahi mila.\n")
        return

    print("\n[+] Sending request...\n")

    api_url = f"https://api-otrss.garena.com/support/callback/?access_token={eat_token}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Mobile)",
        "Accept": "text/html,application/xhtml+xml",
        "Referer": "https://ticket.kiosgamer.co.id/",
        "Connection": "keep-alive"
    }

    try:
        response = requests.get(api_url, headers=headers, allow_redirects=True, timeout=50)

        print(f"[+] Status Code : {response.status_code}")
        print(f"[+] Final URL   : {response.url}\n")

        parsed_final = urllib.parse.urlparse(response.url)
        params = urllib.parse.parse_qs(parsed_final.query)

        # ✅ Success case
        if 'access_token' in params:
            access_token = params['access_token'][0]
            account_id = params.get('account_id', ['Unknown'])[0]
            nickname = urllib.parse.unquote(params.get('nickname', ['Unknown'])[0])
            region = params.get('region', ['Unknown'])[0]

            print("===== SUCCESS =====")
            print(f"Nickname     : {nickname}")
            print(f"Account ID   : {account_id}")
            print(f"Region       : {region}")
            print(f"Access Token :\n{access_token}")
            print("===================\n")

        else:
            print("[-] Access token nahi mila!")
            
            # 🔍 Extra debug
            if "error" in response.url or "err=" in response.url:
                print("[!] Server Error Detected (Token invalid / expired)")
            else:
                print("[!] Unknown response, shayad API block hai")

    except Exception as e:
        print(f"[!] Error: {e}")


if __name__ == "__main__":
    eat_to_access_token()
