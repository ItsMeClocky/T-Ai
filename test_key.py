import urllib.request
import json
import sys

key = "AIzaSyB5ufUWX2HWX7H2vm3cAXNkMJzUEj8YBR8"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
data = json.dumps({
    "contents": [{"parts": [{"text": "Hello"}]}],
    "tools": [{"googleSearch": {}}]
}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as response:
        print("Success:", response.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code, e.read().decode())
except Exception as e:
    print("Error:", e)
