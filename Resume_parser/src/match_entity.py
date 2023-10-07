from dateutil import relativedelta
from datetime import datetime
import re
import pandas as pd
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
import spacy

# nltk.download('wordnet')


def extract_name(nlp, text):
    # Process the text with spaCy
    doc = nlp(text)

    # Initialize an empty dictionary to store the extracted names
    names = {
        'first_name': '',
        'middle_name': '',
        'last_name': ''
    }

    # Look for entities in the text that are labeled as a person (PERSON)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            # Split the entity text into tokens and determine the first, middle, and last names
            tokens = ent.text.split()
            if len(tokens) == 1:
                # If there is only one token, assume it is the first name
                names['first_name'] = tokens[0]
            elif len(tokens) == 2:
                # If there are two tokens, assume the first is the first name and the second is the last name
                names['first_name'] = tokens[0]
                names['last_name'] = tokens[1]
            elif len(tokens) == 3:
                # If there are three tokens, assume the first is the first name, the second is the middle name, and the third is the last name
                names['first_name'] = tokens[0]
                names['middle_name'] = tokens[1]
                names['last_name'] = tokens[2]
            else:
                # If there are more than three tokens, assume the last three are the middle and last name
                names['first_name'] = tokens[0]
                names['middle_name'] = ' '.join(tokens[1:-1])
                names['last_name'] = tokens[-1]

            break

    return names


def extract_contact_info(text):
    # Extract phone number using regular expression
    phone_regex = r'(?:\d[ -.]*){10,15}'
    phone_number = re.findall(phone_regex, text)

    # Extract email address using regular expression
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email = re.findall(email_regex, text)

    contact_info = {
        'phone': phone_number,
        'email': email
    }

    return contact_info


def extract_skills(nlp, resume_text):
    nlp_text = nlp(resume_text)

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]

    # reading the csv file
    data = pd.read_csv("../data/skills.csv")
    
    

    # extract values
    skills = list(data.columns.values)

    skillset = []

    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)

    # check for bi-grams and tri-grams (example: machine learning)
    for chunk in nlp_text.noun_chunks:
        chunk_text = chunk.text.lower().strip()
        if chunk_text in skills:
            skillset.append(chunk_text)

    return [i.capitalize() for i in set([i.lower() for i in skillset])]


def extract_education(nlp, resume_text):
    nlp_text = nlp(resume_text)

    # Split document into sentences
    nlp_text = [token.sent.text.strip() for token in nlp_text]

    # Grad all general stop words
    STOPWORDS = set(stopwords.words('english'))

    # Education Degrees
    EDUCATION = EDUCATION = [
    'BE', 'B.E.', 'B.E', 'BS', 'B.S', 'Bachelor of Engineering',
    'ME', 'M.E', 'M.E.', 'MS', 'M.S', 'Master of Engineering', 'Master of Science',
    'BTECH', 'B.TECH', 'MTECH', 'M.TECH', 'Bachelor of Technology', 'Master of Technology',
    'BCA', 'Bachelor of Computer Applications',
    'BBA', 'Bachelor of Business Administration',
    'MBA', 'Master of Business Administration',
    'BSC', 'Bachelor of Science',
    'MSC', 'Master of Science',
    'MCA', 'Master of Computer Applications',
    'MCM', 'Master of Computer Management',
    'PGDCA', 'Post Graduate Diploma in Computer Applications',
    'BCOM', 'Bachelor of Commerce',
    'MCOM', 'Master of Commerce',
    'CA', 'Chartered Accountant',
    'ICWA', 'Institute of Cost and Works Accountants',
    'CS', 'Company Secretary',
    'MCS', 'Master of Computer Science',
    'MIT', 'Master of Information Technology',
    'MCM', 'Master of Computer Management',
    'PGDIT', 'Post Graduate Diploma in Information Technology',
    'PGDBM', 'Post Graduate Diploma in Business Management',
    'PGDM', 'Post Graduate Diploma in Management',
    'PHD', 'Doctor of Philosophy',
    'MSW', 'Master of Social Work',
    'LLB', 'Bachelor of Laws',
    'LLM', 'Master of Laws',
    'MHRM', 'Master of Human Resource Management',
    'MHM', 'Master of Hospitality Management',
    'PGDHRM', 'Post Graduate Diploma in Human Resource Management',
    'PGDHM', 'Post Graduate Diploma in Hospitality Management',
    'PGDMM', 'Post Graduate Diploma in Marketing Management',
    'PGDFM', 'Post Graduate Diploma in Financial Management',
    'PGDIM', 'Post Graduate Diploma in International Business',
    'PGDIB', 'Post Graduate Diploma in International Business',
    'PGDFTM', 'Post Graduate Diploma in Foreign Trade Management',
    'PGDTM', 'Post Graduate Diploma in Tourism Management',
    'PGDFA', 'Post Graduate Diploma in Fine Arts',
    'PGDMC', 'Post Graduate Diploma in Mass Communication',
    'PGDCA', 'Post Graduate Diploma in Computer Applications',
    'PGDJMC', 'Post Graduate Diploma in Journalism and Mass Communication',
    'PGDFT', 'Post Graduate Diploma in Fashion Technology',
    'PGDMD', 'Post Graduate Diploma in Media and Design',
    'PGDTTM', 'Post Graduate Diploma in Travel and Tourism Management',
    'PGDST', 'Post Graduate Diploma in Software Technology',
    'PGDISM', 'Post Graduate Diploma in Information Systems Management',
    'PGDASL', 'Post Graduate Diploma in Applied Statistics and Computing',
    'PGDPM', 'Post Graduate Diploma in Project Management',
    'PGDBI', 'Post Graduate Diploma in Business Intelligence',
    'PGDIA', 'Post Graduate Diploma in Industrial Automation',
    'PGDSM', 'Post Graduate Diploma in Security Management',
    'PGDFA', 'Post Graduate Diploma in Financial Analytics',
    'PGDCAI', 'Post Graduate Diploma in Cloud and Artificial Intelligence',
    'SLC'
    ]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education

nlp = spacy.load('en_core_web_sm')

def extract_experience(resume_text):
    doc = nlp(resume_text)

    experiences = []
    for sent in doc.sents:
        if 'experience' in sent.text.lower() or 'work' in sent.text.lower():
            for ent in sent.ents:
                if ent.label_ == 'ORG':
                    experiences.append(ent.text)
                    break
    return list(set(experiences))

def get_total_experience(experience_list):
    '''
    Wrapper function to extract total months of experience from a resume
    :param experience_list: list of experience text extracted
    :return: total months of experience
    '''
    exp_ = []
    for line in experience_list:
        experience = re.search(
            r'(?P<fmonth>\w+.\d+)\s*(\D|to)\s*(?P<smonth>\w+.\d+|present)',
            line,
            re.I
        )
        if experience:
            exp_.append(experience.groups())
    total_exp = sum(
        [get_number_of_months_from_dates(i[0], i[2]) for i in exp_]
    )
    total_experience_in_months = total_exp
    return total_experience_in_months


def get_number_of_months_from_dates(date1, date2):
    '''
    Helper function to extract total months of experience from a resume
    :param date1: Starting date
    :param date2: Ending date
    :return: months of experience from date1 to date2
    '''
    if date2.lower() == 'present':
        date2 = datetime.now().strftime('%b %Y')
    try:
        if len(date1.split()[0]) > 3:
            date1 = date1.split()
            date1 = date1[0][:3] + ' ' + date1[1]
        if len(date2.split()[0]) > 3:
            date2 = date2.split()
            date2 = date2[0][:3] + ' ' + date2[1]
    except IndexError:
        return 0
    try:
        date1 = datetime.strptime(str(date1), '%b %Y')
        date2 = datetime.strptime(str(date2), '%b %Y')
        months_of_experience = relativedelta.relativedelta(date2, date1)
        months_of_experience = (months_of_experience.years
                                * 12 + months_of_experience.months)
    except ValueError:
        return 0
    return months_of_experience
