import json

log_file = "/home/clocky/.gemini/antigravity/brain/7f511730-602c-492a-8d62-bd04a7bc92f8/.system_generated/logs/transcript_full.jsonl"
html_content = ""

try:
    with open(log_file, "r") as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get("type") == "USER_INPUT":
                    content = data.get("content", "")
                    if "<!DOCTYPE html>" in content and "tclockworkModal" in content:
                        # Extract everything between <USER_REQUEST> and </USER_REQUEST>
                        start = content.find("<!DOCTYPE html>")
                        end = content.rfind("</html>") + len("</html>")
                        if start != -1 and end != -1 and end > start:
                            html_content = content[start:end].strip()
                        else:
                            html_content = content[start:].strip()
            except Exception:
                pass

    if html_content:
        with open("/home/clocky/T-Ai/index.html", "w") as out:
            out.write(html_content)
        print(f"Recovered index.html: {len(html_content)} bytes")
    else:
        print("Could not find the HTML content in the logs.")
except Exception as e:
    print("Error:", e)
