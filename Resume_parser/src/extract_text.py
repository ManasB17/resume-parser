import tika
import re
from tika import parser
import chardet
tika.initVM()


def extract_text_from_resume(file_path):
    # print("Type:",type(file_path))
    # encoding = chardet.detect(file_path.read())
    # print("EncodingL:", encoding)
    results = parser.from_file(file_path)
    document_text = results['content']
    
    # with open(file_path, 'rb') as file_obj:
    #     response = tika.parser.from_file(file_obj)
    
    document_text = remove_metadata(document_text)
    return document_text

def remove_metadata(text):
    # Define regular expressions to match metadata and unwanted generic strings
    # regex_list = []
    try:
        regex_list = [
            r'^Title:.*$',
            r'^Author:.*$',
            r'^CreationDate:.*$',
            r'^ModDate:.*$',
            r'^Producer:.*$',
            r'^Keywords:.*$',
            r'^Subject:.*$',
            r'^Content-Type:.*$',
            r'^Resume.*$',
            r'^CV.*$',
        ]
        
        # Remove matching patterns from the text
        for regex in regex_list:
            text = re.sub(regex, '', text, flags=re.MULTILINE)
        
    except:
        print("Error: could not remove metadata")
    return text.strip()
