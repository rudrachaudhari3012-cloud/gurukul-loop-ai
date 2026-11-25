
import os
from google import genai

# Google Gemini API Key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Please set your GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

# AI Coach Instructions
SYSTEM_PROMPT = """
You are AB SCHOOL LOOP AI Coach.

You are a friendly, intelligent school assistant.

Your responsibilities:
1. Help students understand school subjects.
2. Explain difficult topics in easy language.
3. Help students with homework.
4. Generate quizzes and practice questions.
5. Give study tips and motivation.
6. Help students improve their learning.
7. Give step-by-step explanations.
8. Be polite, friendly and encouraging.

Rules:
- Use simple English.
- Give examples wherever possible.
- Encourage students to think independently.
- Never make students feel bad for asking questions.
- Keep answers suitable for school students.
"""

# Start AI Chat
chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "system_instruction": SYSTEM_PROMPT,
        "temperature": 0.7
    }
)

print("================================")
print("   AB SCHOOL LOOP AI COACH")
print("================================")
print("Hello Student! I am your AI Coach.")
print("Ask me anything about your studies.")
print("Type 'exit' to stop.\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        print("AI Coach: Keep learning! Best of luck!")
        break

    try:
        response = chat.send_message(question)

        print("\nAI Coach:", response.text)
        print("--------------------------------")

    except Exception as error:
        print("Something went wrong:", error)
