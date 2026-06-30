import requests
import json

url = "http://127.0.0.1:5000/predict"
payload = {"url": "http://ex.com/search?q=<script>alert('hacked')</script>"}
headers = {"Content-Type": "application/json"}

print("Sending request to Python ML Service...")
try:
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.text)
except Exception as e:
    print("Request failed:", e)
