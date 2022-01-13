# imports
import tempfile
from PIL import Image
import os
import pdfplumber

fontboolmagic = False


def writee(char):
    global x, y, bg, yPos
    if char == '\n':
        x = 75
        y += 50
        yPos+=50
    elif char=='space':
        cases = Image.open(
                "myfont/space.png")
        bg.paste(cases, (x, y))
        size = cases.width
        x += size
        del cases
    else:
        char.lower()
        if not fontboolmagic:
            cases = Image.open(
                "myfont/%s.png" % char)
            bg.paste(cases, (x, y))
            size = cases.width
            x += size
            del cases
        else:
            tempPath = os.path.join(os.path.join(
                tempfile.gettempdir(), "tempfont"), '%s.png' % char)
            cases = Image.open(tempPath)
            bg.paste(cases, (x, y))
            size = cases.width
            x += size
            del cases


def letterwrite(word, sizeOfSheet, allowedChars):
    global x, y, yPos,pgNumber,pageHeight,bg
    
    if pageHeight-yPos<=170:
        # print("Word hit: ",word)
        tmpPath = os.path.join(tempfile.gettempdir(),"%dout.png"%pgNumber)
        bg.save(tmpPath)
        pgNumber+=1
        x=75
        y=50
        yPos=50
        bg1 = Image.open("myfont/bg.png")
        bg = bg1

    if x > sizeOfSheet - 35*(len(word)):        
        x = 75
        y += 50
        yPos+=50
    for letter in word:
        if letter in allowedChars:
            if letter.islower():
                pass
            elif letter.isupper():
                letter = letter.lower()
                letter += 'upper'
            elif letter == '.':
                letter = "fullstop"
            elif letter == '!':
                letter = 'exclamation'
            elif letter == '?':
                letter = 'question'
            elif letter == ',':
                letter = 'comma'
            elif letter == '(':
                letter = 'leftparenthesis'
            elif letter == ')':
                letter = 'rightparenthesis'
            elif letter == '-':
                letter = 'minus'
            elif letter == '[':
                letter = 'leftsquarebracket'
            elif letter == ']':
                letter = 'rightsquarebracket'
            elif letter == ';':
                letter = 'semicolon'
            elif letter == ':':
                letter = 'colon'
            elif letter == '"':
                letter = 'doubleinvertedcomma'
            elif letter == "'":
                letter = 'singleinvertedcomma'
            elif letter == '+':
                letter = 'plus'
            elif letter == '=':
                letter = 'equal'
            elif letter == '/':
                letter = 'slash'
            elif letter == '&':
                letter = 'ampersand'
            elif letter == '%':
                letter = 'percentage'
            writee(letter)


def worddd(Input, sizeOfSheet, allowedChars):
    wordlist = Input.split(' ')
    for i in wordlist:
        letterwrite(i, sizeOfSheet, allowedChars)
        writee('space')


def magicWand(filePath, extension, fontbool):

    print("Filepath is: ", filePath)
    print("Extension is: ", extension)
    global bg, x, y, fontboolmagic, yPos, pageHeight, pgNumber
    fontboolmagic = fontbool
    if fontboolmagic:
        print("Font uploaded!!")
    bg = Image.open("myfont/bg.png")
    sizeOfSheet = bg.width
    pageHeight = bg.height
    pgNumber=0
    x, y = 75, 50
    yPos = 50

    allowedChars = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j',
                    'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M',
                    ',', '.', '-', '?', '!', '(', ')', '"', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '\n', ' ', "'", ';', ':', '/', '%', '&', '[', ']']

    data = ""

    if extension == "txt":
        with open(filePath, 'r') as file:
            dataT = file.read()
            data += dataT
        file.close()
    elif extension == "pdf":
        with pdfplumber.open(r''+filePath) as file:
            for page in file.pages:
                dataTemp = page.extract_text()
                data += dataTemp
        file.close()
    else:
        print("Extension not supported!!")

    os.remove(filePath)

    # Here we do a dynamic operation to print the data
    wordList = data.split(' ')
    for i in wordList:
        letterwrite(i,sizeOfSheet,allowedChars)
        writee('space')

    tmpPath = os.path.join(tempfile.gettempdir(),"%dout.png"%pgNumber)
    bg.save(tmpPath)

    if fontboolmagic:
        for imgs in os.listdir(os.path.join(tempfile.gettempdir(), "tempfont")):
            os.remove(os.path.join(os.path.join(
                tempfile.gettempdir(), "tempfont"), imgs))
        os.rmdir(os.path.join(tempfile.gettempdir(), "tempfont"))
        fontboolmagic = False
