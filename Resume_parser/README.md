Resume parser
==============================

This is a simple resume parser created using Python and Spacy library. This parser extracts the name, contact information, skills, education, and experience from a given resume.

## **Files**

1. **`stremlit_app.py`**: The main file that contains the Streamlit application to display the extracted information.
2. **`extract_text.py`**: This file contains the function to extract text from a resume file.
3. **`match_entity.py`**: This file contains the functions to extract the name, contact information, skills, education, and experience from the resume text.

## **How to use**

1. Clone the repository.
2. Install the necessary libraries mentioned in the requirements.txt file.
3. Place the resume file in the **`data/Resume/`** directory.
4. Run the Streamlit app using the following command: **`streamlit run streamlit_app.py`**.
5. Enter the resume file name in the text input.
6. The extracted information will be displayed on the Streamlit app.
## **Future Work**

1. Improving the accuracy of the parser by training the Spacy model on more data.
2. Adding more features to extract additional information from the resume.
3. Converting the parser into a Fast API for easy integration with other applications.