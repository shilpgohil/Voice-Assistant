from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import pyttsx3

# Initialize the Flask app
app = Flask(__name__)

# Initialize the text-to-speech engine
engine = pyttsx3.init()  # This sets up pyttsx3 TTS engine

# Gemini API Key
GEMINI_API_KEY = 'AIzaSyDMtUt-8CiPGEAp_SGpqrsWFGHe-AyTCPw'  # Replace with your valid Gemini key

# Route to stop ongoing TTS
@app.route("/stop_speaking", methods=["POST"])
def stop_speaking():
    global engine
    if engine._inLoop:  # Check if the engine is currently speaking
        engine.stop()
    return jsonify({"status": "speaking stopped"})

# Predefined Q&A responses
predefined_qa = {
    "what should we know about your life story in a few sentences?": "I come from a background where curiosity was always encouraged more than just scoring marks. From tinkering with tech as a teenager to diving deep into AI and data, my journey has always been about exploring how things work and how they can be made better. I’m someone who learns by building and failing, then improving until I get it right.",
    "what’s your #1 superpower?": "My biggest strength is adaptability. Whether it’s switching between different tech stacks or adjusting to fast changing environments, I stay calm, observe quickly, and align myself with what’s needed. I don’t get stuck – I evolve.",
    "what are the top 3 areas you’d like to grow in?": "People Skills: I want to become better at leading teams and understanding different working styles.\n\nBusiness Thinking: I’m learning to look at problems not just from a tech angle but also from a customer and ROI perspective.\n\nSystem Design & Scale: I want to deepen my understanding of building large, reliable systems in the AI + data space.",
    "what misconception do your coworkers have about you?": "Some people think I’m always serious or too focused – but once they get to know me, they realise I’m actually quite fun, collaborative, and always ready to crack a joke or lighten the mood when needed.",
    "how do you push your boundaries and limits?": "I deliberately take on projects or roles that are slightly out of my comfort zone – ones that force me to stretch and learn fast. I also seek feedback often, reflect deeply, and believe in showing up every day, especially when things get uncomfortable – that’s where real growth happens."
}

# Personal data dictionary for bot reference
personal_data = {
    "name": "Shilp Gohil",
    "contact": {
        "phone": "+91 9328418263",
        "email": "shilpgohil@gmail.com",
        "github": "https://github.com/shilpgohil",
        "linkedin": "https://linkedin.com/in/shilp gohil-23b371166"
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

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Route to handle incoming user questions
@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json['question']
    reply = ""

    # Check predefined Q&A
    for question, answer in predefined_qa.items():
        if user_input.lower().strip() == question.lower():
            reply = answer
            break

    # Check from personal data
    if not reply:
        if "name" in user_input.lower():
            reply = f"My name is {personal_data['name']}."
        elif any(keyword in user_input.lower() for keyword in ["contact", "phone", "email", "github", "linkedin"]):
            contact_info = personal_data['contact']
            reply = f"You can reach me at phone: {contact_info['phone']}, email: {contact_info['email']}, GitHub: {contact_info['github']}, or LinkedIn: {contact_info['linkedin']}."
        elif "summary" in user_input.lower() or "experience" in user_input.lower():
            reply = personal_data['summary']
        elif "education" in user_input.lower():
            edu = personal_data['education'][0]
            reply = f"I have a {edu['degree']} from {edu['institution']} in {edu['location']}, from {edu['years']}."
        elif "skills" in user_input.lower():
            skills_list = [f"{category.replace('_', ' ').title()}: {', '.join(skills)}" for category, skills in personal_data['skills'].items()]
            reply = "My skills include: " + "; ".join(skills_list) + "."
        elif "projects" in user_input.lower():
            projects_info = [f"{p['title']} ({p['year']}): {p['description']} (Tech: {', '.join(p['tech'])})" for p in personal_data['projects']]
            reply = "Here are some of my projects: " + "; ".join(projects_info) + "."

    # If nothing matches, use Gemini API
    if not reply:
        prompt = f"Act like Shilp Gohil and answer this question: {user_input}"
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        reply = response.text

    # Speak out the response using pyttsx3
    engine.say(reply)
    engine.runAndWait()

    return jsonify({"answer": reply})

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
