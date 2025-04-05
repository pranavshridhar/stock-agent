import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Verify available models
print("✅ SDK Version:", genai.__version__)
print("✅ Models Available:")
for model in genai.list_models():
    print("→", model.name)

# Use Gemini Pro
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

user_profile = {
    "experience": "beginner",
    "risk_tolerance": "medium",
    "goals": "long-term growth"
}

instruction = f"You are an AI investment coach. This user is a {user_profile['experience']} investor with {user_profile['risk_tolerance']} risk tolerance and aims for {user_profile['goals']}."

chat_history = [
    {"role": "user", "parts": [f"{instruction}"]}
]

while True:
    prompt = input("You: ")
    if prompt.lower() in ("exit", "quit"):
        print("👋 Goodbye!")
        break

    chat_history.append({"role": "user", "parts": [prompt]})
    response = model.generate_content(chat_history)
    chat_history.append({"role": "model", "parts": [response.text]})

    print("\n🤖 Gemini says:\n", response.text)