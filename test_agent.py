import requests
import json

def test_agent(prompt):
    url = "http://127.0.0.1:8080/invocations"
    payload = {"prompt": prompt}
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print("Full Response:")
        print("=" * 50)
        print(result['result'])
        print("=" * 50)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_agent("What is the latest score of mancity team?")