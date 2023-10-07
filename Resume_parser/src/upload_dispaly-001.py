import streamlit as st
import spacy
from extract_resume_info import driver
from extract_text import extract_text_from_resume

nlp = spacy.load('en_core_web_trf')

st.title('Resume parser')

def upload_file():
    uploaded_file = st.file_uploader("Upload file:", type=(['pdf', 'doc', 'docx']))
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        st.write(file_details)
        file_contents = uploaded_file.read()
        extract_content = extract_text_from_resume(file_contents)
        return st.write(file_contents)

file = upload_file()

def display_content(file):
    result = driver(file)
    return result

def main():
    st.write(display_content(file))