from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

# Check if TTS should be enabled (i.e., running locally)
USE_TTS = os.environ.get("USE_TTS", "true").lower() == "true"
engine = None

if USE_TTS:
    try:
        import pyttsx3
        engine = pyttsx3.init()
    except Exception as e:
        print("pyttsx3 init failed:", e)
        engine = None

# Initialize Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")

# Gemini API Key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDMtUt-8CiPGEAp_SGpqrsWFGHe-AyTCPw")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/stop_speaking", methods=["POST"])
def stop_speaking():
    global engine
    if engine and engine._inLoop:
        engine.stop()
    return jsonify({"status": "speaking stopped"})

def generate_audio(text):
    if engine:
        engine.say(text)
        engine.runAndWait()

# ... [Rest of your predefined_qa, personal_data dictionary same as before] ...

# Main interaction route
@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("question", "").strip().lower()
    reply = ""

    for question, answer in predefined_qa.items():
        if user_input == question.lower():
            reply = answer
            break

    if not reply:
        if "name" in user_input:
            reply = f"My name is {personal_data['name']}."
        elif any(key in user_input for key in ["contact", "phone", "email", "github", "linkedin"]):
            c = personal_data["contact"]
            reply = f"Phone: {c['phone']}, Email: {c['email']}, GitHub: {c['github']}, LinkedIn: {c['linkedin']}"
        elif "summary" in user_input or "experience" in user_input:
            reply = personal_data["summary"]
        elif "education" in user_input:
            edu = personal_data["education"][0]
            reply = f"{edu['degree']} from {edu['institution']}, {edu['location']} ({edu['years']})"
        elif "skills" in user_input:
            skill_lines = [f"{k.replace('_', ' ').title()}: {', '.join(v)}" for k, v in personal_data["skills"].items()]
            reply = "My skills include: " + "; ".join(skill_lines)
        elif "projects" in user_input:
            proj_lines = [f"{p['title']} ({p['year']}): {p['description']} [Tech: {', '.join(p['tech'])}]" for p in personal_data["projects"]]
            reply = "Some of my projects: " + "; ".join(proj_lines)

    if not reply:
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"Act like Shilp Gohil and answer this: {user_input}")
            reply = response.text
        except Exception as e:
            print("Gemini error:", e)
            reply = "Sorry, I'm having trouble processing that right now."

    generate_audio(reply)
    return jsonify({"answer": reply})

# Local launch
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
