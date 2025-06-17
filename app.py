from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

# Load Gemini API Key securely
GEMINI_API_KEY = os.environ.get("AIzaSyDMtUt-8CiPGEAp_SGpqrsWFGHe-AyTCPw")

app = Flask(__name__)

# Personality setup
predefined_qa = {
    "what should we know about your life story in a few sentences?": "I come from a background where curiosity was always encouraged...",
    "what’s your #1 superpower?": "My biggest strength is adaptability...",
    "what are the top 3 areas you’d like to grow in?": "People Skills, Business Thinking, System Design & Scale...",
    "what misconception do your coworkers have about you?": "Some people think I’m always serious...",
    "how do you push your boundaries and limits?": "I take on slightly uncomfortable projects..."
}

personal_data = {
    "name": "Shilp Gohil",
    "contact": {
        "phone": "+91 9328418263",
        "email": "shilpgohil@gmail.com",
        "github": "https://github.com/shilpgohil",
        "linkedin": "https://linkedin.com/in/shilp gohil-23b371166"
    },
    "summary": "Skilled software development engineer...",
    "education": [{
        "institution": "Sathyabama University",
        "degree": "B.Tech in Information Technology",
        "location": "Chennai, India",
        "years": "2019 – 2023"
    }],
    "experience": [...],  # Keep your actual data here
    "skills": {...},      # Same here
    "projects": [...]     # And here
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get('question', '').lower().strip()
    reply = ""

    # 1. Predefined Q&A
    for question, answer in predefined_qa.items():
        if user_input == question.lower():
            reply = answer
            break

    # 2. Personal Data Fallback
    if not reply:
        if "name" in user_input:
            reply = f"My name is {personal_data['name']}."
        elif any(k in user_input for k in ["contact", "phone", "email", "github", "linkedin"]):
            c = personal_data["contact"]
            reply = f"You can reach me at phone: {c['phone']}, email: {c['email']}, GitHub: {c['github']}, or LinkedIn: {c['linkedin']}."
        elif "summary" in user_input or "experience" in user_input:
            reply = personal_data["summary"]
        elif "education" in user_input:
            edu = personal_data["education"][0]
            reply = f"I have a {edu['degree']} from {edu['institution']} in {edu['location']} ({edu['years']})."
        elif "skills" in user_input:
            reply = "My skills include: " + "; ".join(
                f"{k.replace('_', ' ').title()}: {', '.join(v)}" for k, v in personal_data["skills"].items()
            ) + "."
        elif "projects" in user_input:
            reply = "Here are my projects: " + "; ".join(
                f"{p['title']} ({p['year']}): {p['description']} (Tech: {', '.join(p['tech'])})"
                for p in personal_data["projects"]
            )

    # 3. Use Gemini if no matches
    if not reply and GEMINI_API_KEY:
        try:
            prompt = f"Act like Shilp Gohil and answer this: {user_input}"
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            reply = response.text
        except Exception as e:
            reply = "Sorry, Gemini API failed. Try again later."

    return jsonify({"answer": reply})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
