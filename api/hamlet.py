import random
import re
import os
from nltk.tokenize import sent_tokenize
import numpy as np

def removeJunk(text):
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

def chunkQuotes(text):
    """
    text: list of sentences, including names like HAMLET
    returns: 2d list of quote chunks
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

def filterLength(quoteChunks, n):
    """
    quoteChunks: 2d list containing lists of strings which are lines
    n: minimum number of lines in each id
    Returns an array containing only quotes that are at least n lines long
    """
    filteredQuotes = list()

    for quotes in quoteChunks:
        if len(quotes) >= n:
            filteredQuotes.append(quotes)
    return filteredQuotes

def cleanNames(s):
    for name in names:
        if name == "All" or name == "OTHER":
            continue
        s = re.sub(r"\b" + name.lower() + r"\b", "_____", s, flags=re.IGNORECASE)
    return s


def filter_paragraph_length(paragraphs: list[str], word_count):
    return ["\n".join(p) for p in paragraphs if len("\n".join(p).split()) >= word_count]

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
    generates an ID for Hamlet given the minimum number of lines
    Args:
        n (int): minimum number of lines

    Returns:
        str: the generated ID
    """
    global quotes
    quote = generate_id(quotes, int(n))
    if hide_names:
        return cleanNames(quote)
    return quote