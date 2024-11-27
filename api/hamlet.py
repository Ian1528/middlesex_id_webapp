import random
import re
import os
def wordCountBlockLines(text):
    count = 0
    for word in " ".join(text).split():
        count += 1
    return count

def removeJunk(text):
    text_clean = list()
    for line in text:
        addLine = True
        lowercase = line.lower()
        if "act" in lowercase or line.isnumeric() or line == "" or lowercase == "dies" or "scene " in lowercase or "exeunt" in lowercase or lowercase == "sings":
            addLine = False
        if "=" in line or "Enter" in line or "Exit" in line or "Re-enter" in line or "Exeunt" in line or "Enter Ghost" in line or "Enter KING" in line:
            addLine = False
        if line in names:
            text_clean.append("NAMEHERE") # still want to keep track of names
        if len(line) > 0 and (line[0] == '[' or line[-1] == ']'):
            addLine = False
        # takes care of cases like "Enter Ghost" and "Enter KING"
        for name in names:
            if name in line:
                addLine = False
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
        if name == "All":
            continue
        s = re.sub(r"\b" + name + r"\b", "_____", s, flags=re.IGNORECASE)
    return s

def getID(quoteChunks):
    block = random.choice(quoteChunks) # first choose a random block of sentences
    stringQuote = "\n".join(block)

    totalWords = wordCountBlockLines(block)
    # if the quote isn't long enough, just return it
    if (totalWords < 50):
        return stringQuote

    startWordIndex = random.randint(0, totalWords - 50)

    # find index of where the sentence should start
    lastSentenceIndex = 0
    punct = [".", "!", "?"]
    wordCount = 0
    for i in range(len(stringQuote)):
        char = stringQuote[i]
        if char == "\n" or char == " ":
            wordCount += 1
        elif char in punct:
            lastSentenceIndex = i+1
        if wordCount == startWordIndex:
            break
    finalID = ""
    wordCount = 0

    punct = [".", "!", "?", ";"]
    for i in range(lastSentenceIndex, len(stringQuote)):
        # go from the start of the sentence to the end of the whole quote
        char = stringQuote[i]
        finalID += char
        if char == "\n" or char == " ":
            wordCount += 1
        if char in punct and wordCount > 30: # end of sentence and word count is large enough
            return cleanNames(finalID)
    

file_path = os.path.join(os.path.dirname(__file__), 'hamlet_textfile.txt')
names = ["PRINCE FORTINBRAS", "First Player", "Messenger", "Second Player", "HAMLET", "HORATIO", "First Clown", "Second Clown", "KING CLAUDIUS", "CLAUDIUS", "POLONIUS", "Ghost", "GHOST", "LORD POLONIUS", "LAERTES", "ROSENCRANTZ", "GUILDENSTERN", "OSRIC", "VOLTIMAND", "CORNELIUS", "MARCELLUS", "BARNARDO", "FRANCISCO", "REYNALDO", "FORTINBRAS", "QUEEN GERTRUDE", "OPHELIA", "All", "Servant", "Sailors", "Captain", "QUEEN", "KING", "father", "mother", "Gertrude", "Gravedigger"]

f = open(file_path, 'r')

text = f.read()
text = text.split("\n")

text_clean = removeJunk(text)
quotes = chunkQuotes(text_clean)


def generate_Hamlet_ID(n: int) -> str:
    """
    generates an ID for Hamlet given the minimum number of lines
    Args:
        n (int): minimum number of lines

    Returns:
        str: the generated ID
    """
    global quotes
    if n == 0:
        return "Please enter a number greater than 0"
    quotes = filterLength(quotes, int(n))
    return getID(quotes)