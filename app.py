from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()
app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

SYSTEM_PROMPT = """You are Career Guide AI.
Only answer questions related to: career choices, skills, learning roadmaps, internships, resumes, job preparation, and career planning.
If a question is unrelated, politely say you can only help with your specific domain.
Keep answers simple, practical, and beginner-friendly.
For high-stakes topics, recommend checking current official sources or a qualified professional.
"""

@app.route("/")
def home():
    return render_template("index.html", bot_name="Career Guide AI")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({"reply": "Please enter a question."})
    if not client:
        return jsonify({"reply": "Gemini API key is not configured. Add GEMINI_API_KEY in Render Environment Variables."})
    prompt = SYSTEM_PROMPT + "\nUser question: " + message
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )
        return jsonify({"reply": getattr(response, "text", None) or "I could not generate a response."})
    except Exception as e:
        print("Gemini error:", e)
        return jsonify({"reply": "AI service error. Check your Gemini API key, model availability, and Render logs."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
