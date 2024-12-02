from nltk.tokenize import sent_tokenize
import random
import re
import numpy as np
import os

def remove_names(s, names):
    for name in names:
        s = re.sub(r"\b" + name + r"\b", "_____", s, flags=re.IGNORECASE)
    return s

def clean_text(text: str):
    text_list_form = text.split("\n")
    text_clean = ""
    bad_characters = ["[", "]", "{", "}", "(", ")", "/", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    for line in text_list_form:
        if len(line) == 0 or line[0] == " ":
            continue
        if "BOOK" in line or "CHAPTER" in line or "THE ILIAD" in line or "HOMER" in line:
            continue
        if line[0] in bad_characters or line[-1] in bad_characters:
            continue
        if line.isnumeric():
            continue
        text_clean += line + "\n"
    return text_clean

def filter_paragraph_length(paragraphs: list[str], word_count):
    return [p for p in paragraphs if len(p.split()) >= word_count]

def generate_id(paragraphs: list[str], word_count):
    filtered_paragraphs = filter_paragraph_length(paragraphs, word_count)
    paragraph = random.choice(filtered_paragraphs)

    sentences = sent_tokenize(paragraph)
    sentence_lengths = [len(s.split()) for s in sentences]

    for end_index in range(len(sentences)-1, -1, -1):
        if sum(sentence_lengths[end_index:]) >= word_count:
            break
    
    index = np.random.randint(0, end_index+1)
    final_quote = ""
    while len(final_quote.split()) < word_count:
        final_quote += sentences[index] + " "
        index += 1
    return final_quote

def generate_general_ID(n: int, filename: str, names: list[str]) -> str:
    file_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(file_path, encoding="utf8")

    text = f.read()
    text = clean_text(text)
    paragraphs = text.split("\n\n")

    id_with_names = generate_id(paragraphs, n)
    return remove_names(id_with_names, names)