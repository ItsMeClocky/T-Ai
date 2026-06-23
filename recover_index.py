import json
import glob
import os

largest_content = ""
for log_file in glob.glob("/home/clocky/.gemini/antigravity/brain/*/.system_generated/logs/*.jsonl"):
    try:
        with open(log_file, "r") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if data.get("type") == "TOOL_CALL":
                        calls = data.get("tool_calls", [])
                        for call in calls:
                            name = call.get("function_name", "")
                            args = call.get("args", {})
                            
                            # Check write_to_file
                            if name == "default_api:write_to_file" and str(args.get("TargetFile", "")).endswith("index.html"):
                                content = args.get("CodeContent", "")
                                if len(content) > len(largest_content):
                                    largest_content = content
                            
                            # Check replace_file_content
                            elif name == "default_api:replace_file_content" and str(args.get("TargetFile", "")).endswith("index.html"):
                                content = args.get("ReplacementContent", "")
                                if len(content) > len(largest_content):
                                    largest_content = content
                except Exception:
                    pass
    except Exception as e:
        print(e)

if largest_content:
    with open("index_recovered.html", "w") as out:
        out.write(largest_content)
    print(f"Recovered {len(largest_content)} bytes")
else:
    print("No index.html found in write_to_file calls.")
