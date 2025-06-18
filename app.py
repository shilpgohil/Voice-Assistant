from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDMtUt-8CiPGEAp_SGpqrsWFGHe-AyTCPw")

@app.route("/")
def home():
    return render_template("index.html")

predefined_qa = {
    "what should we know about your life story in a few sentences?": "I come from a background where curiosity was always encouraged more than just scoring marks. From tinkering with tech as a teenager to diving deep into AI and data, my journey has always been about exploring how things work and how they can be made better. I’m someone who learns by building and failing, then improving until I get it right.",
    "what’s your #1 superpower?": "My biggest strength is adaptability. Whether it’s switching between different tech stacks or adjusting to fast changing environments, I stay calm, observe quickly, and align myself with what’s needed. I don’t get stuck — I evolve.",
    "what are the top 3 areas you’d like to grow in?": "People Skills: I want to become better at leading teams and understanding different working styles.\n\nBusiness Thinking: I’m learning to look at problems not just from a tech angle but also from a customer and ROI perspective.\n\nSystem Design & Scale: I want to deepen my understanding of building large, reliable systems in the AI + data space.",
    "what misconception do your coworkers have about you?": "Some people think I’m always serious or too focused — but once they get to know me, they realise I’m actually quite fun, collaborative, and always ready to crack a joke or lighten the mood when needed.",
    "how do you push your boundaries and limits?": "I deliberately take on projects or roles that are slightly out of my comfort zone — ones that force me to stretch and learn fast. I also seek feedback often, reflect deeply, and believe in showing up every day, especially when things get uncomfortable — that’s where real growth happens."
}

personal_data = {
    "name": "Shilp Gohil",
    "contact": {
        "phone": "+91 9328418263",
        "email": "shilpgohil@gmail.com",
        "github": "https://github.com/shilpgohil",
        "linkedin": "https://linkedin.com/in/shilpgohil-23b371166"
    },
    "summary": "Skilled software development engineer with experience in delivering scalable applications using Python, Java, and C++ across AWS and GCP environments. Recognised for integrating AI and machine learning.",
    "education": [
        {
            "institution": "Sathyabama University",
            "degree": "B.Tech in Information Technology",
            "location": "Chennai, India",
            "years": "2019 – 2023"
        }
    ],
    "experience": [
        {
            "title": "Machine Learning QA Intern",
            "company": "Pioneer Solutions Pvt. Ltd.",
            "location": "Ahmedabad, India",
            "years": "2023–2024",
            "responsibilities": [
                "Built automated pipelines for data validation and model inference testing using Pytest, reducing QA time by 10+ hrs/week.",
                "Validated ML models for financial risk prediction, resolving issues in model accuracy, data drift, and edge cases."
            ]
        },
        {
            "title": "Research Assistant",
            "company": "International Research Center (IRC), Sathyabama University",
            "location": "Hybrid",
            "years": "2022–2023",
            "responsibilities": [
                "Boosted text classification F1 score from 0.78 to 0.88 via data preprocessing, model tuning, and pipeline optimization.",
                "Analyzed usability of AI tools using quantitative feedback, contributing to internal reports and academic papers."
            ]
        },
        {
            "title": "Public Relations Officer",
            "company": "Microsoft Student Club, Sathyabama University",
            "location": "Chennai, India",
            "years": "2021–2022",
            "responsibilities": [
                "Led 10+ workshops/hackathons on ML, Cloud, and Coding, increasing participation by 40%.",
                "Prototyped a Python-Dialogflow chatbot and brought in industry speakers on Azure, GitHub, and Power Platform."
            ]
        }
    ],
    "skills": {
        "programming": ["Python", "C", "C++", "SQL"],
        "machine_learning_ai": ["Machine Learning", "Deep Learning", "Generative AI", "Agent AI", "Computer Vision", "LLMs", "Prompt Engineering"],
        "frameworks_tools": ["TensorFlow", "PyTorch", "OpenCV", "LangChain", "Streamlit", "Docker", "Git", "CI/CD"],
        "web_backend": ["Django", "Flask", "Streamlit", "MongoDB", "RESTful APIs"],
        "cloud_devops": ["Azure", "GCP", "AWS", "Kubernetes", "Qwiklabs"],
        "data_analysis_visualisation": ["Preprocessing", "Statistical Analysis", "Tableau", "Power BI", "matplotlib"],
        "collaboration_research": ["Agile", "Documentation", "User Testing", "Teamwork"],
        "interpersonal": ["Leadership", "Communication", "Problem Solving", "Mentoring", "Adaptability"]
    },
    "projects": [
        {
            "title": "Mathematical Agent",
            "tech": ["Streamlit", "Google Gemini", "ChromaDB"],
            "year": 2025,
            "description": "AI driven math assistant with step-by-step solutions in algebra, calculus & advanced topics."
        },
        {
            "title": "Computer Vision Data Annotator",
            "tech": ["OpenCV", "Pillow"],
            "year": 2025,
            "description": "Smart video to frame converter with AI tagging, retry logic, and progress tracking."
        },
        {
            "title": "LLM Powered Web Scraper",
            "tech": ["BeautifulSoup", "LangChain", "Docker", "Kubernetes"],
            "year": 2024,
            "description": "Python-based scraper achieving 88% classification accuracy."
        }
    ]
}

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
    return jsonify({"answer": reply})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
