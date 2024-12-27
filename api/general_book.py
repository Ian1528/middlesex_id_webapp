from nltk.tokenize import sent_tokenize
import docx
import random
import re
import numpy as np
import os
import json

def remove_names(s: str, names: list[str]) -> str:
    """
    Blurs names in the text

    Args:
        s (str): string to remove names from
        names (list[str]): list of names to remove

    Returns:
        str: cleaned string
    """
    for name in names:
        s = re.sub(r"\b" + name + r"\b", "_____", s, flags=re.IGNORECASE)
    return s

def clean_text(text: str) -> str:
    """
    Cleans a list of text lines by removing unwanted characters and lines.
    
    Args:
        text (list[str]): A list of strings representing lines of text to be cleaned.
   
    Returns:
        str: A single string containing the cleaned text, with each line separated by a newline character.
    
    """
    text_list_form = text.split("\n")
    text_clean = ""
    bad_characters = ["[", "]", "{", "}", "(", ")", "/", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    for line in text_list_form:
        if len(line) == 0 or line[0] == " " or line[0] == "":
            text_clean += "\n"
            continue
        if "BOOK" in line or "CHAPTER" in line:
            continue
        if line[0] in bad_characters or line[-1] in bad_characters:
            continue
        if line.isnumeric():
            continue
        if line[0].isnumeric() and line[-1].isnumeric():
            continue
        text_clean += line + "\n"
    return text_clean

def filter_paragraph_length(paragraphs: list[str], word_count: int) -> list[str]:
    """
    Filters paragraphs based on a minimum word count.

    Args:
        paragraphs (list[str]): A list of paragraphs, where each paragraph is a string.
        word_count (int): The minimum number of words a paragraph must have to be included in the result.
    
    Returns:
        list[str]: A list of paragraphs that meet or exceed the minimum word count.
    """
    return [p for p in paragraphs if len(p.split()) >= word_count]

def generate_id(paragraphs: list[str], word_count: int) -> str:
    """
    Generates an ID from a list of paragraphs with a specified word count. 

    Helper function for all API endpoints that generate IDs.

    Args:
        paragraphs (list[str]): list of paragraphs to generate the ID from.
        word_count (int): minimum word count of the ID.
    
    Returns:
        str: generated ID.
    """
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

def generate_custom_ID(n: int, file_path: str, names: list[str]) -> str:
    """
    Generates an ID from a custom uploaded text file with a specified word count.

    Args:
        n (int): minimum word count of the ID.
        file_path (str): path to the custom uploaded text file.
        names (list[str]): list of names to remove from the ID.
    
    Returns:
        str: generated ID.
    """
    curr_path = os.path.dirname(__file__)
    parent_path = os.path.split(curr_path)[0]
    absolute_file_path = os.path.join(parent_path, file_path)
    f = open(absolute_file_path, encoding="utf8")

    text = f.read()
    text = clean_text(text)
    paragraphs = text.split("\n\n")

    id_with_names = generate_id(paragraphs, n)
    return remove_names(id_with_names, names)

def generate_general_public_ID(n: int, filename: str, names: list[str]) -> str:
    """
    Generates an ID from one of the textfiles in the public directory of the app.
    Args:
        n (int): The number of IDs to generate.
        filename (str): The name of the file containing the text to process.
        names (list[str]): A list of names to be removed from the generated ID.
    Returns:
        str: The generated ID with specified names removed.
    """

    curr_path = os.path.dirname(__file__)
    parent_path = os.path.split(curr_path)[0]
    file_path = os.path.join(parent_path, f'public/{filename}')
    f = open(file_path, encoding="utf8")

    text = f.read()
    text = clean_text(text)
    paragraphs = text.split("\n\n")

    id_with_names = generate_id(paragraphs, n)
    return remove_names(id_with_names, names)

def generate_thecolony_id(n: int, names: list[str]) -> str:
    """
    Generates an ID from thecolony.json with a specified word count.

    This differs from other generate_id functions because it
    takes IDs across paragraphs from multiple speakers.

    Args:
        n (int): minimum word count of the ID.
        names (list[str]): names to remove from the ID.

    Returns:
        str: the generated ID
    """
    file_path = os.path.join(os.path.dirname(__file__), 'thecolony.json')
    with open(file_path, "r") as f:
        paragraphs = json.load(f)
    i = np.random.randint(0, len(paragraphs)) # paragraph index counter
    final_quote = ""
    while len(final_quote.split()) < n:
        paragraph = paragraphs[i]
        sentences = sent_tokenize(paragraph)
        sentence_lengths = [len(s.split()) for s in sentences]

        for end_index in range(len(sentences)-1, -1, -1):
            if sum(sentence_lengths[end_index:]) >= n:
                break
        
        index = np.random.randint(0, end_index+1)
        for index in range(len(sentences)):
            final_quote += sentences[index] + " "
            if len(final_quote.split()) > n:
                return remove_names(final_quote, names)
        i += 1
        final_quote += "\n"
    return remove_names(final_quote, names)

def generate_json_file_id(n: int, file_name: str, names: list[str]) -> str:
    """
    Generates an ID from a JSON file that contains a list of paragraphs.

    Args:
        n (int): minimum word count of the ID.
        file_name (str): path to the JSON file.
        names (list[str]): names to remove from the ID.

    Returns:
        str: the generated ID.
    """
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, "r") as f:
        paragraphs = json.load(f)
    id_with_names = generate_id(paragraphs, n)
    return remove_names(id_with_names, names)


def docx_to_text_string(word_doc_path: str) -> str:
    """
    Converts a Word document to a string.

    Args:
        word_doc_path (str): path to the Word document.

    Returns:
        str: the text content of the Word document.
    """
    doc = docx.Document(word_doc_path)
    txt = ""
    for para in doc.paragraphs:
        if para.text == "":
            continue
        txt += para.text + "\n" + "\n"
    return txt
