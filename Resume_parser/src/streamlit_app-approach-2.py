import spacy
import sys, fitz
import streamlit as st

file_name = st.text_input(
        "Enter file name 👇")

st.header('Resume_parser')
model = spacy.load('../models/model/output/model-best')
fname = f'../data/Resume/{file_name}'
doc = fitz.open(fname)
text = " "

for page in doc:
  text = text + str(page.get_text())

doc = model(text)
for ent in doc.ents:
    st.subheader(ent.label_)
    st.write(ent.text)
