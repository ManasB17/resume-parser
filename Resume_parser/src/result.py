import spacy
import sys, fitz

model = spacy.load('../models/model/output/model-best')
fname = '../data/Resume/selpdf.pdf'
doc = fitz.open(fname)
text = " "

for page in doc:
  text = text + str(page.get_text())

doc = model(text)
for ent in doc.ents:
  print(ent.text, "   >>>>",ent.label_)