import random
import re
import os
from nltk.tokenize import sent_tokenize
import numpy as np

def removeJunk(text: list[str]) -> list[str]:
    """
    Removes junk lines from the text file

    Args:
        text (list[str]): List of lines from the text file
    
    Returns:
        list[str]: List containing cleaned lines
    """
    text_clean = list()
    for line in text:
        addLine = True
        lowercase = line.lower()
        if "act" in lowercase or line.isnumeric() or line == "" or lowercase == "dies" or "scene " in lowercase or "exeunt" in lowercase or lowercase == "sings":
            addLine = False
        if "=" in line or "Enter" in line or "Exit" in line or "Re-enter" in line or "Exeunt" in line or "Enter Ghost" in line or "Enter KING" in line:
            addLine = False
        # takes care of cases like "Enter Ghost" and "Enter KING"
        for name in names:
            if line.strip().find(name.upper()) == 0:
                # case where name and speech are same line, i.e.
                # BARNARDO  Who's there!
                text_clean.append("NAMEHERE")
                rest_of_line = line[len(name):]
                if len(rest_of_line) > 0:
                    text_clean.append(rest_of_line)
                addLine = False # because we already added it, we don't need to keep going
                break
        if addLine:
            text_clean.append(line)
    return text_clean

def chunkQuotes(text: list[str]) -> list[list[str]]:
    """
    Splits the text into quotes from different characters

    Args:
        text (list[str]): list of lines from the text

    Returns:
        list[list[str]]: list of quotes from different characters
    """

    allQuotes = list()

    chunk = list()
    for line in text:
        if line != "NAMEHERE":
            chunk.append(line)
        else:
            allQuotes.append(chunk)
            chunk = list()
    return allQuotes

def cleanNames(s: str) -> str:
    """
    Blurs names in the text

    Args:
        s (str): text to be cleaned

    Returns:
        str: cleaned text
    """
    for name in names:
        if name == "All" or name == "OTHER":
            continue
        s = re.sub(r"\b" + name.lower() + r"\b", "_____", s, flags=re.IGNORECASE)
    return s


def filter_paragraph_length(paragraphs: list[list[str]], word_count: int) -> list[str]:
    """
    Filters paragraphs based on a minimum word count.
    Args:
        paragraphs (list[list[str]]): A list of paragraphs, where each paragraph is a list of strings (lines).
        word_count (int): The minimum number of words a paragraph must have to be included in the result.
    Returns:
        list[str]: A list of paragraphs (as single strings) that meet or exceed the minimum word count.
    """

    return ["\n".join(p) for p in paragraphs if len("\n".join(p).split()) >= word_count]

def generate_id(paragraphs: list[list[str]], word_count: int) -> str:
    """
    Generates a quote from a list of paragraphs with a specified word count.
    Args:
        paragraphs (list[list[str]]): A list of paragraphs, where each paragraph is a list of sentences.
        word_count (int): The minimum word count for the generated quote.
    Returns:
        str: A quote with the specified word count.
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

file_path = os.path.join(os.path.dirname(__file__), 'hamlet_textfile.txt')
names = ["PRINCE FORTINBRAS", "First Player", "Messenger", "Second Player", "HAMLET", "HORATIO", "First Clown", "Second Clown", "KING CLAUDIUS", "CLAUDIUS", "POLONIUS", "Ghost", "GHOST", "LORD POLONIUS", "LAERTES", "ROSENCRANTZ", "GUILDENSTERN", "OSRIC", "VOLTIMAND", "CORNELIUS", "MARCELLUS", "OTHER", "BARNARDO", "FRANCISCO", "REYNALDO", "FORTINBRAS", "QUEEN GERTRUDE", "OPHELIA", "All", "Servant", "Sailors", "Captain", "QUEEN", "KING", "Gertrude", "Gravedigger", "GENTLEMAN", "SAILOR", "DOCTOR", "AMBASSADOR", "LORD", "PLAYER KING", "PLAYER QUEEN", "PLAYER"]
lowercase_names = [name.lower() for name in names]
f = open(file_path, 'r')

text = f.read()
text = re.sub(r'\[.*?\]', '', text)
text = text.split("\n")

text_clean = removeJunk(text)
quotes = chunkQuotes(text_clean)


def generate_Hamlet_ID(n: int, hide_names: bool) -> str:
    """
    Generates an ID for Hamlet given the minimum number of lines. Called by the API.
    Args:
        n (int): minimum number of words

    Returns:
        str: the generated ID
    """
    global quotes
    quote = generate_id(quotes, int(n))
    if hide_names:
        return cleanNames(quote)
    return quote