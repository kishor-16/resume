from flask import Flask, render_template, request
import os
from resume_parser import extract_skills, match_skills

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Upload and skill matching
@app.route("/upload", methods=["POST"])
def upload_resume():
    if 'resume' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['resume']
    job_skills_input = request.form.get('job_skills', '')
    job_skills = [skill.strip() for skill in job_skills_input.split(',') if skill.strip()]
    
    if file.filename == "":
        return "No selected file", 400

    # Ensure uploads folder exists
    upload_dir = "../uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    upload_path = os.path.join(upload_dir, file.filename)
    file.save(upload_path)
    
    # Extract and match skills
    resume_skills = extract_skills(upload_path)
    matched, score = match_skills(resume_skills, job_skills)
    
    result = {
        'matched': ", ".join(matched) if matched else "No skills matched",
        'score': score
    }
    
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
