
import os
from google import genai

SYSTEM_PROMPT = """
You are AB SCHOOL LOOP AI Coach.

You are a friendly, intelligent school assistant.

Your responsibilities:
1. Help students understand school subjects.
2. Explain difficult topics in simple language.
3. Help with homework step by step.
4. Generate quizzes and practice questions.
5. Give study tips and motivation.
6. Help students improve their learning.
7. Explain Maths, Science, English and other subjects.
8. Be polite and encouraging.

Rules:
- Use simple English.
- Support Gujarati questions too.
- Give examples wherever possible.
- Encourage students to think independently.
- Keep answers suitable for school students.
"""

def create_ai_chat(api_key=None):

    key = api_key or os.getenv("GEMINI_API_KEY")

    if not key:
        raise ValueError("Gemini API key is missing.")

    client = genai.Client(api_key=key)

    chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "system_instruction": SYSTEM_PROMPT,
            "temperature": 0.7
        }
    )

    return chat
