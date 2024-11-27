from nltk.tokenize import sent_tokenize
import random
import numpy as np
import re

def clean_text(text):
    text_clean = ""
    bad_characters = ["[", "]", "{", "}", "(", ")", "/", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    for line in text:
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

def split_sentences(text):
    return sent_tokenize(text)


def generate_ID(sentences, starting_index):
    index = starting_index
    sample = sentences[index]
    while len(sample.split()) < 50:
        index += 1
        if index == len(sentences):
            return ""
        sample += " " + sentences[index]
    return sample

def get_ID(text: str, n: int) -> str:
    
    sentences = split_sentences(text)
    index = np.random.randint(0, len(sentences)-n)
    sample = generate_ID(sentences, index)

    # handle edge case of the end of the novel
    while sample == "":
        index = np.random.randint(0, len(sentences)-n)
        sample = generate_ID(sentences, index)
    sample_without_names = cleanNames(sample)
    return sample_without_names
        
def cleanNames(s):
    for name in names:
        s = re.sub(r"\b" + name + r"\b", "_____", s, flags=re.IGNORECASE)
    return s


f = open("C:/Users/Sneez/OneDrive/Desktop/Coding/Visual Studio Code/School/MX_Id_generator/iliad_edited.txt", encoding="utf8")
names = ["ACHILLES", "AGAMEMNON", "HECTOR", "HELEN", "MENELAUS", "PARIS", "PATROCLUS", "PRIAM", "ZEUS", "HERA", "ATHENA", "APOLLO", "POSEIDON", "HERMES", "THETIS", "CALCHAS", "ANDROMACHE", "ASTYANAX", "BRISIES", "CHRYSEIS", "HECUBA", "ODYSSEUS"]
text = f.read().split("\n")

text = clean_text(text)

def generate_Iliad_ID(n: str) -> str:
    global text
    return get_ID(text, int(n))