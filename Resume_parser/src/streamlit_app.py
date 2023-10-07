import spacy
import re
import streamlit as st
from extract_text import extract_text_from_resume
from match_entity import (
    extract_name,
    extract_contact_info,
    extract_skills,
    extract_education,
    extract_experience,
    get_total_experience
)


def main(file_name:str):
    """main _summary_

    Parameters
    ----------
    file_name : str
        file name with extension.
    """
    # loading model
    nlp = spacy.load('en_core_web_trf')
    file_path = f'../data/Resume/{file_name}'
    extracted_text = extract_text_from_resume(file_path)
    doc = nlp(extracted_text)
    text = " ".join(
        [token.text for token in doc if not token.is_stop and not token.is_punct])
    clean_text = re.sub('\s+', ' ', text).strip()

    names = extract_name(nlp, clean_text)
    st.subheader('Name')
    if names['middle_name'] == '':
        st.write(names['first_name'], names['last_name'])
    else:
        st.write(names['first_name'], names['middle_name'], names['last_name'])

    contact = extract_contact_info(clean_text)
    st.subheader('Contact Information')
    st.write(contact)

    skills = extract_skills(nlp, clean_text)
    st.subheader('Skills')
    st.write(skills)

    education = extract_education(nlp, clean_text)
    st.subheader('Education')
    st.write(education)

    experience = extract_experience(clean_text)
    st.subheader('Experience')
    st.write(experience)


if __name__ == "__main__":
    st.header('Resume Parser')
    text_input = st.text_input(
        "Enter file name 👇")
    main(text_input)
