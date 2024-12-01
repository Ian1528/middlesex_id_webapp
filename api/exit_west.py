import nltk
nltk.download('punkt', download_dir="/tmp/nltk_data")

from nltk.tokenize import sent_tokenize
import random
import re
import numpy
import os

def remove_names(s, names):
    for name in names:
        s = re.sub(r"\b" + name + r"\b", "_____", s, flags=re.IGNORECASE)
    return s

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
    
    index = random.randint(0, end_index)

    final_quote = ""
    while len(final_quote.split()) < word_count:
        final_quote += sentences[index] + " "
        index += 1
    return final_quote

file_path = os.path.join(os.path.dirname(__file__), 'exit_west_textfile.txt')
f = open(file_path, encoding="utf8")

text = f.read()
text = remove_names(text, ["Saeed", "Nadia"])
paragraphs = text.split("\n\n")

def generate_exit_west_ID(n: int) -> str:
    return generate_id(paragraphs, n)