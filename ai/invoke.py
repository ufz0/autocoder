import requests
import json

def generate(input_text: str) -> str:
    url = "https://internet.com:8000/messages"
    request_body = json.dumps({"message": input_text})
    
    try:
        # Set a timeout of 5 seconds for the request
        response = requests.post(url, data=request_body, headers={"Content-Type": "application/json"}, timeout=5)
        
        if response.status_code == 429:
            print("Quota exceeded. Stopping requests.")
            return "Quota exceeded"

        response.raise_for_status()
        return response.json().get("answer", "")
    
    except requests.RequestException as e:
        print(f"Error generating message: {e}")
        return ""