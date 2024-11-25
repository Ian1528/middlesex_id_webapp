import random
import re
def wordCountBlockLines(text):
    count = 0
    for word in " ".join(text).split():
        count += 1
    return count

def removeJunk(text):
    text_clean = list()
    for line in text:
        addLine = True
        if "Act" in line or line.isnumeric() or line == "" or line == "Dies" or "Scene " in line or "Exeunt" in line or line == "Sings":
            addLine = False
        if line in names:
            text_clean.append("NAMEHERE") # still want to keep track of names
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
        s = re.sub(name, "_____", s, flags=re.I)
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
        if char in punct and wordCount > 45: # end of sentence and word count is large enough
            return cleanNames(finalID)



f = open("hamlet.txt", "r")
names = ["PRINCE FORTINBRAS", "First Player", "Messenger", "Second Player", "HAMLET", "HORATIO", "First Clown", "Second Clown", "KING CLAUDIUS", "CLAUDIUS", "POLONIUS", "Ghost", "LORD POLONIUS", "LAERTES", "ROSENCRANTZ", "GUILDENSTERN", "OSRIC", "VOLTIMAND", "CORNELIUS", "MARCELLUS", "BERNARDO", "FRANCISCO", "REYNALDO", "FORTINBRAS", "QUEEN GERTRUDE", "OPHELIA", "All", "Servant", "Sailors", "Captain"]

text = f.read()
text = text.split("\n")

text_clean = removeJunk(text)
quotes = chunkQuotes(text_clean)
numLines = 0
while numLines == 0:
    try:
        numLines = int(input("How many mininum lines for each ID? "))
    except:
        print("Not valid input")

quotes = filterLength(quotes, numLines)

again = "yes"

while again == "yes" or again == "y":
    print()
    print(getID(quotes))
    print()
    again = input("Again? ").lower()