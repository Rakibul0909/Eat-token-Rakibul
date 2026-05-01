import requests
import urllib.parse

def eat_api_debug():

    print("\n=== EAT API DEBUG TOOL ===\n")

    user_input = input("Enter EAT Token OR Full URL: ").strip()

    # 🔍 Extract token
    eat_token = None
    if "http" in user_input:
        parsed = urllib.parse.urlparse(user_input)
        params = urllib.parse.parse_qs(parsed.query)
        eat_token = params.get("eat", [None])[0]
    else:
        eat_token = user_input

    if not eat_token:
        print("\n[!] EAT token nahi mila!\n")
        return

    api_url = f"https://api-otrss.garena.com/support/callback/?access_token={eat_token}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Mobile)",
        "Accept": "*/*",
        "Referer": "https://ticket.kiosgamer.co.id/",
        "Connection": "keep-alive"
    }

    print("\n[+] Sending request...\n")

    try:
        response = requests.get(api_url, headers=headers, allow_redirects=True, timeout=60)

        # 🔹 Basic info
        print("===== BASIC INFO =====")
        print(f"Status Code : {response.status_code}")
        print(f"Final URL   : {response.url}")
        print("======================\n")

        # 🔹 Headers
        print("===== RESPONSE HEADERS =====")
        for k, v in response.headers.items():
            print(f"{k}: {v}")
        print("============================\n")

        # 🔹 Raw text
        print("===== RAW RESPONSE =====")
        print(response.text[:2000])  # limit to avoid spam
        print("========================\n")

        # 🔹 Try JSON
        try:
            json_data = response.json()
            print("===== JSON RESPONSE =====")
            print(json_data)
            print("=========================\n")
        except:
            print("[!] JSON format nahi hai\n")

        # 🔹 Extract params from final URL
        parsed_final = urllib.parse.urlparse(response.url)
        final_params = urllib.parse.parse_qs(parsed_final.query)

        if final_params:
            print("===== EXTRACTED PARAMS =====")
            for key, value in final_params.items():
                print(f"{key} : {value[0]}")
            print("============================\n")

    except requests.exceptions.Timeout:
        print("[!] Request timeout ho gaya (server slow/block)")
    except Exception as e:
        print(f"[!] Error: {e}")


if __name__ == "__main__":
    eat_api_debug()
