import docx
import os
from general_book import clean_text

curr_path = os.path.dirname(__file__)
parent_path = os.path.split(curr_path)[0]
file_path = os.path.join(parent_path, f'public/{"tewwg.docx"}')

def docx_to_text_string(word_doc_path: str) -> str:
    doc = docx.Document(word_doc_path)
    txt = ""
    for para in doc.paragraphs:
        if para.text == "":
            continue
        txt += para.text + "\n" + "\n"
    return txt

text = docx_to_text_string(file_path)
text = clean_text(text)
paragraphs = text.split("\n\n")
print(paragraphs[0:5])
