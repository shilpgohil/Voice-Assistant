from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

# Check if running locally
IS_LOCAL = os.environ.get("RENDER") is None

# Flask App
app = Flask(__name__)

# Text-to-Speech (only local)
if IS_LOCAL:
    import pyttsx3
    engine = pyttsx3.init()

# Gemini API Key
GEMINI_API_KEY = 'AIzaSyDMtUt-8CiPGEAp_SGpqrsWFGHe-AyTCPw'  # Replace with valid key

# Stop speech endpoint (only local)
@app.route("/stop_speaking", methods=["POST"])
def stop_speaking():
    if IS_LOCAL and engine._inLoop:
        engine.stop()
    return jsonify({"status": "speaking stopped"})

# Predefined responses
predefined_qa = {
    "what should we know about your life story in a few sentences?": "I come from a background where curiosity was always encouraged...",
    "what’s your #1 superpower?": "My biggest strength is adaptability...",
    "what are the top 3 areas you’d like to grow in?": "People Skills: I want to become better at leading teams...",
    "what misconception do your coworkers have about you?": "Some people think I’m always serious...",
    "how do you push your boundaries and limits?": "I deliberately take on projects that are slightly out of my comfort zone..."
}

# Personal data
personal_data = {
    "name": "Shilp Gohil",
    "contact": {
        "phone": "+91 9328418263",
        "email": "shilpgohil@gmail.com",
        "github": "https://github.com/shilpgohil",
        "linkedin": "https://linkedin.com/in/shilpgohil-23b371166"
    },
    "summary": "Skilled software development engineer with experience...",
    "education": [
        {
            "institution": "Sathyabama University",
            "degree": "B.Tech in Information Technology",
            "location": "Chennai, India",
            "years": "2019 – 2023"
        }
    ],
    "experience": [],  # Simplified
    "skills": {
        "programming": ["Python", "C", "C++", "SQL"],
        "machine_learning_ai": ["Machine Learning", "Deep Learning", "Generative AI"],
        "frameworks_tools": ["TensorFlow", "PyTorch", "OpenCV"],
        "web_backend": ["Django", "Flask", "Streamlit"],
        "cloud_devops": ["Azure", "GCP", "AWS"],
        "data_analysis_visualisation": ["Tableau", "Power BI"],
        "interpersonal": ["Leadership", "Communication"]
    },
    "projects": [
        {
            "title": "Mathematical Agent",
            "tech": ["Streamlit", "Google Gemini", "ChromaDB"],
            "year": 2025,
            "description": "AI driven math assistant..."
        }
    ]
}

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Ask route
@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json['question']
    reply = ""

    # Predefined answers
    for question, answer in predefined_qa.items():
        if user_input.lower().strip() == question.lower():
            reply = answer
            break

    # Personal info responses
    if not reply:
        text = user_input.lower()
        if "name" in text:
            reply = f"My name is {personal_data['name']}."
        elif any(k in text for k in ["contact", "phone", "email", "github", "linkedin"]):
            c = personal_data['contact']
            reply = f"You can reach me at phone: {c['phone']}, email: {c['email']}, GitHub: {c['github']}, or LinkedIn: {c['linkedin']}."
        elif "summary" in text or "experience" in text:
            reply = personal_data['summary']
        elif "education" in text:
            e = personal_data['education'][0]
            reply = f"I have a {e['degree']} from {e['institution']} in {e['location']} ({e['years']})."
        elif "skills" in text:
            skills = [f"{k.replace('_', ' ').title()}: {', '.join(v)}" for k, v in personal_data['skills'].items()]
            reply = "My skills include: " + "; ".join(skills) + "."
        elif "projects" in text:
            reply = "Here are some of my projects: " + "; ".join([
                f"{p['title']} ({p['year']}): {p['description']} (Tech: {', '.join(p['tech'])})"
                for p in personal_data['projects']
            ]) + "."

    # Gemini fallback
    if not reply:
        prompt = f"Act like Shilp Gohil and answer this question: {user_input}"
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        reply = response.text

    # Speak if local
    if IS_LOCAL:
        engine.say(reply)
        engine.runAndWait()

    return jsonify({"answer": reply})

# Start the app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
