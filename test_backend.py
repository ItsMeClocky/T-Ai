import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import api_keys

def test_chatgpt():
    print("Testing ChatGPT (OpenAI) with a simple prompt...")
    messages = [{"role": "user", "content": "Ciao, sei online?"}]
    result = api_keys._try_openai("gpt-4o-mini", messages)
    print("ChatGPT Result:", result.get("gpt_available", False))
    print("ChatGPT Response:", str(result.get("response", ""))[:150] + "...")
    if result.get("errors"):
        print("ChatGPT Errors:", result.get("errors"))

def test_pollinations():
    print("\nTesting Pollinations code model (claude-fable-5)...")
    messages = [{"role": "user", "content": "Scrivi un codice python semplice."}]
    result = api_keys._pollinations_post(messages)
    print("Pollinations Model Used:", result.get("model"))
    print("Pollinations Response:", str(result.get("response", ""))[:150] + "...")

    print("\nTesting Pollinations image model (nanobanana)...")
    messages = [{"role": "user", "content": "Disegna un gatto."}]
    result = api_keys._pollinations_post(messages)
    print("Pollinations Model Used:", result.get("model"))
    print("Pollinations Response:", str(result.get("response", ""))[:150] + "...")

if __name__ == "__main__":
    test_chatgpt()
    test_pollinations()
