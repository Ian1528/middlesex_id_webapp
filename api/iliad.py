from nltk.tokenize import sent_tokenize
import numpy as np
import re
import os

def clean_text(text: list[str]):
    text_clean = ""
    bad_characters = ["[", "]", "{", "}", "(", ")", "/", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    for line in text:
        if len(line) == 0 or line[0] == " ":
            continue
        if "BOOK" in line or "CHAPTER" in line or "THE ILIAD" in line or "HOMER" in line:
            continue
        if line[0] in bad_characters or line[-1] in bad_characters:
            continue
        if line.isnumeric() or line.isupper():
            continue
        text_clean += line + "\n"
    return text_clean

def split_sentences(text):
    return sent_tokenize(text)


def generate_ID(sentences, starting_index, n):
    index = starting_index
    sample = sentences[index]
    while len(sample.split()) < n:
        index += 1
        if index == len(sentences):
            return ""
        sample += " " + sentences[index]
    return sample

def get_ID(text: str, n: int, hide_names: bool) -> str:
    
    sentences = split_sentences(text)
    index = np.random.randint(0, len(sentences))
    sample = generate_ID(sentences, index, n)

    # handle edge case of the end of the novel
    while sample == "":
        index = np.random.randint(0, len(sentences))
        sample = generate_ID(sentences, index)
    if hide_names:
        return cleanNames(sample)
    return sample
        
def cleanNames(s):
    for name in names + ["swift runner", "horse breaker"]:
        s = re.sub(r"\b" + name + r"\b", "_____", s, flags=re.IGNORECASE)
    return s

file_path = os.path.join(os.path.dirname(__file__), 'iliad_textfile.txt')
f = open(file_path, encoding="utf8")

names = ["ACHILLES", "AGAMEMNON", "HECTOR", "HELEN", "MENELAUS", "PARIS", "PATROCLUS", "PRIAM", "ZEUS", "HERA", "ATHENA", "APOLLO", "POSEIDON", "HERMES", "THETIS", "CALCHAS", "ANDROMACHE", "ASTYANAX", "BRISIES", "CHRYSEIS", "HECUBA", "ODYSSEUS", "DIOMEDES"]
text = f.read().split("\n")

text = clean_text(text)

def generate_Iliad_ID(n: str, hide_names: bool) -> str:
    global text
    return get_ID(text, int(n), hide_names)
