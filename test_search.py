import urllib.request
import json

key = "AIzaSyB5ufUWX2HWX7H2vm3cAXNkMJzUEj8YBR8"
url = f"https://customsearch.googleapis.com/customsearch/v1?key={key}&q=test"
req = urllib.request.Request(url)
try:
    with urllib.request.urlopen(req) as response:
        print("Success:", response.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code, e.read().decode())
except Exception as e:
    print("Error:", e)
