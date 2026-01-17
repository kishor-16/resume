import pdfplumber
import re


def extract_skills(file_path):
    skills_list = [
        'Python', 'Java', 'C++', 'JavaScript', 'React', 'Flask', 
        'Node', 'SQL', 'HTML', 'CSS'
    ]
    
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + " "
    
    found_skills = [skill for skill in skills_list if re.search(r'\b'+skill+r'\b', text, re.IGNORECASE)]
    
    if not found_skills:
        return []
    return found_skills


def match_skills(resume_skills, job_skills):
    matched = [skill for skill in resume_skills if skill in job_skills]
    score = round(len(matched) / len(job_skills) * 100, 2) if job_skills else 0
    return matched, score
