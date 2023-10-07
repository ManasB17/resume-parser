import spacy
import re
from extract_text import extract_text_from_resume
from match_entity import (
    extract_name,
    extract_contact_info,
    extract_skills,
    extract_education,
    extract_experience,
    get_total_experience
)


def main():
    # loading model
    nlp = spacy.load('en_core_web_trf')
    file_path = '../data/Resume/selpdf.pdf'
    extracted_text = extract_text_from_resume(file_path)
    doc = nlp(extracted_text)
    text = " ".join(
        [token.text for token in doc if not token.is_stop and not token.is_punct])
    clean_text = re.sub('\s+', ' ', text).strip()

    names = extract_name(nlp, clean_text)
    if names['middle_name'] == '':
        print(f"Name :{names['first_name'], names['last_name']}")
    else:
        print(f"Name :{names['first_name'], names['middle_name'], names['last_name']}")

    contact = extract_contact_info(clean_text)
    print(f"Contact :{contact}")

    skills = extract_skills(nlp, clean_text)
    print(f"Skills :{skills}")

    education = extract_education(nlp, clean_text)
    print(f"Education :{education}")

    experience = extract_experience(clean_text)
    print(f"Experience :{experience}")

if __name__ == "__main__":
    main()
