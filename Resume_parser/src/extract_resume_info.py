import spacy
import re
import json
from match_entity import (
    extract_name,
    extract_contact_info,
    extract_skills,
    extract_education,
    extract_experience,
    get_total_experience
)
from extract_text import extract_text_from_resume

nlp = spacy.load('en_core_web_trf')

def get_clean_txt(file_path):

    extracted_text = extract_text_from_resume(file_path)
    
    doc = nlp(extracted_text)
    text = " ".join(
        [token.text for token in doc if not token.is_stop and not token.is_punct])
    clean_text = re.sub('\s+', ' ', text).strip()
    
    return clean_text.encode('ascii', errors='replace').replace(b"?",b" ")

def extract_resume_info(resume_text):
    # Extract the name from the resume
    name = extract_name(nlp, resume_text)

    # Extract the contact information from the resume
    contact_info = extract_contact_info(resume_text)

    # Extract the skills from the resume
    skills = extract_skills(nlp, resume_text)

    # Extract the education from the resume
    education = extract_education(nlp, resume_text)

    # Extract the experience from the resume
    experience = extract_experience(resume_text)

    # Combine the information into a dictionary
    resume_info = {
        'name': name,
        'contact_info': contact_info,
        'skills': skills,
        'education': education,
        'experience': experience
    }

    return resume_info

# Define a function to extract information from multiple resumes
# def extract_resumes_info(resumes):
#     # Initialize an empty list to store the extracted information
#     resumes_info = []

#     # Loop through each resume and extract the information
#     for resume in resumes:
#         resume_info = extract_resume_info(resume)
#         resumes_info.append(resume_info)

#     return resumes_info

# infos = extract_resume_info(clean_text)
# print(infos)

def driver(file_path):
    clean_text = get_clean_txt(file_path)
    result = extract_resume_info(clean_text)
    return json.dumps(result)
