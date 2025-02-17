import requests

def main():
    url = "http://127.0.0.1:8000/drug_count"
    payload = {"drug": "Lepirudin"}
    response = requests.post(url, json=payload)
    print("Status code:", response.status_code)
    print("Response JSON:", response.json())

if __name__ == "__main__":
    main()