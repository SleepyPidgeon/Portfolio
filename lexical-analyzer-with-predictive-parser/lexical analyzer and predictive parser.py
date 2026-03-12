#The Following is code used for Lexical Analysis
import os
import sys

#Takes user input and checks if the file exists, also locates filename as script directory
def fileVerification(s):
    fileName = s
    validName = False
    while(validName == False):
        s_dir = os.path.dirname(os.path.abspath(__file__))
        f_path = os.path.join(s_dir, fileName)
        if(os.path.isfile(f_path)):
            validName = True
            return f_path
        else:
           fileName = input("Invalid file name! Try again: ")

#Token values for keywords, symbols and actions
IDENTIFIER = "ID"
KEYWORD = 11
INT = "INT"
SYMBOL = 30
VALID = 31
COMMENT = 95
ERROR = 99
LETTER = 1
NUM = 2
#A List of Valid Symbols for the Grammar of the MiniLanguage
symbol_list = [':','.',',',';','<','=','>','+','-','*','(',')']
#List of Keywords for the Grammar of the MiniLanguage
keyWords = ["program","bool","int","if","then","else","end","while","do","print","or","mod", "and", "not","false","true"]

row = 1
column = 1
index = 0
charKind = 0
lex = "z"
cChar = ' '
lexLen = 0
nToken = 0
endOfFile = None

fileName = input("Please enter a file name: ")
fileName = fileVerification(fileName)
with open(fileName, 'r') as file:
    content = file.read()

#This block sets the boundaries of how many rows and the character size of each row for the file
lines = content.splitlines()
lineSizes = [None]*len(lines)
for i in range(len(lineSizes)):
    lineSizes[i]=len(lines[i])
totalLines = len(lines)
rowIndex = 0
charsRead = 0

#Calls for the next character in the file
def callChar():
    global index
    global cChar
    global charKind

    if len(content) > index:
        cChar = content[index]
        index += 1
    else:
        cChar = None
        index += 1

    if cChar != endOfFile:
        if cChar.isalpha():
            charKind = LETTER
        elif cChar.isdigit():
            charKind = NUM
        else:
            charKind = SYMBOL
    else:
        charKind = endOfFile

#Adds the next character to the lexeme
def pushChar():
    global lex
    if lex == " ":
        lex = cChar
    else:
        lex = lex + cChar

#Defines the position of the lexeme
def position():
    global row
    global rowIndex
    global column
    global charsRead

    column = index  - charsRead 
    
    if(rowIndex < totalLines):
        if(column > lineSizes[rowIndex]):
            column = 1
            row += 1
            charsRead += lineSizes[rowIndex] + 1
            rowIndex +=1
            if(rowIndex < totalLines):
                while(lineSizes[rowIndex]==0):
                    row+=1
                    charsRead = charsRead + lineSizes[rowIndex] + 1
                    rowIndex +=1

#If a comment indiciator "#" is found, the rest of the line is skipped
def skipComments():
    global index
    index = index + (lineSizes[rowIndex] - column + 1)

#Builds the lexeme based on the grammar of the language, displays the lexeme and its associated information if necessary
def next():
    global lex
    global charKind
    global nToken
    global column
    lex = " "
    lexLen = 0

    if(charKind == endOfFile or cChar == "."):
        charKind = None
        nToken = endOfFile
        return nToken
    
    else:
        if(charKind != endOfFile):
            while cChar.isspace():
                callChar()
                if(cChar == None):
                    nToken = endOfFile
                    break
            position()

        while(cChar=="/"):
            pushChar()
            callChar()
            if(cChar == "/"):
                position()
                pushChar()
                skipComments()
                position()
                lex = " "
                callChar()
            else:
                nToken == SYMBOL
                charKind = None
        
        if(charKind != endOfFile):
            while cChar.isspace():
                callChar()
                if(cChar == None):
                    nToken = endOfFile
                    break
            position()


        if charKind == LETTER:
            position()
            nToken = None
            pushChar()
            callChar()
            while((charKind == LETTER) or (charKind == NUM) or (cChar == "_")):
                pushChar()
                callChar()
        
            #Checks for keywords in the lex
            for i in range (len(keyWords)):
                if(lex == keyWords[i]):
                    nToken = KEYWORD

            if(nToken != KEYWORD):
                nToken = IDENTIFIER
        
        #If the lex is a numeric value, numbers are continued to be added until the character is no longer a number
        elif charKind == NUM:
            position()
            pushChar()
            callChar()
            while(charKind == NUM):
                pushChar()
                callChar()
            nToken = INT

        #If the lex is a symbol it will be deduced if the symbol is valid or not
        elif charKind == SYMBOL:
            position()
            nToken = None
            pushChar()
            callChar()
            if(lex == "!"):
                if(charKind == SYMBOL and cChar == "="):
                    pushChar()
                    callChar()
                    nToken = VALID
                else:
                    nToken = ERROR
            else:
                for j in range(len(symbol_list)):
                    if (lex == symbol_list[j]):
                        nToken = VALID
                        if(lex == ":"):
                            if(charKind == SYMBOL and cChar == "="):
                                pushChar()
                                callChar()
                                break
                        elif(lex == "="):
                            if(charKind == SYMBOL and cChar == "<"):
                                pushChar()
                                callChar()
                                break
                        elif(lex == ">"):
                            if(charKind == SYMBOL and cChar == "="):
                                pushChar()
                                callChar()
                                break
                        else:
                            break
                    else:
                        nToken = ERROR

#The following is the code used for the Top-down predictive parser
root = None
c1 = None
c2 = None
c3 = None

def main():
    next()
    program()


#Program method
def program():
    match("program")
    match(IDENTIFIER)
    match(":")
    body()
    match(".")
    print("true")

#match method
def match(sym):
    if(lex == sym or nToken == sym):
        next()
    else:
        print("Error! I see '",lex,"' at Position", str(row)+":"+str(column),". But i expected","'"+sym+"'")
        print("false")
        sys.exit(0)
#Body method
def body():
    if(lex == "bool" or lex == "int"):
        declarations()
    statements()

#Declarations method
def declarations():
    declaration()
    while(lex == "bool" or lex == "int"):
        declaration()

#Declaration method
def declaration():
    assert(lex == "bool" or lex == "int"),"Error found at "+str(row)+":"+str(column)+ " should be bool or int"
    next()
    match(IDENTIFIER)
    while (lex == ","):
        next()
        match(IDENTIFIER)
    match(";")

#statements method
def statements():
    statement()
    while(lex == ";"):
        next()
        statement()

#statement method
def statement():
    if(nToken == IDENTIFIER):
        assignment()
    elif(lex == "if"):
        conditional()
    elif(lex == "while"):
        iterative()
    elif(lex == "print"):
        printStatement()
    else:
        expected([IDENTIFIER, "if","while","print"])

#Expected method
def expected(sym_set):
    sym_here = False
    for g in range(len(sym_set)):
        if (lex == sym_set[g] or nToken == sym_set[g]):
            sym_here = True
            break
    if(sym_here == False):
        print("ERROR at Position",str(row)+":"+str(column), "Expected to find one of the following", sym_set, "but i see","'",lex,"'")
        print("false")
        sys.exit(0)


#method for assignment statements
def assignment():
    assert(nToken == "ID"),"Error found at "+str(row)+":"+str(column)+ " should be an IDENTIFIER"
    match(IDENTIFIER)
    match(":=")
    expression()

#method for conditional statement
def conditional():
    assert(lex == "if"), "Error found at "+str(row)+":"+str(column)+ " should be 'if'"
    match("if")
    expression()
    match("then")
    body()
    if(lex == "else"):
        next()
        body()
    match("end")

#method for Expression
def expression():
    sExpression()
    if(lex == "<" or lex == "=<" or lex == "=" or lex == "!=" or lex == ">=" or lex == ">"):
        next()
        sExpression()

#method for Simple Expressions
def sExpression():
    term()
    while(lex == "+" or lex == "-" or lex == "or"):
        next()
        term()

#Method for terms
def term():
    factor()
    while(lex == "*" or lex == "/" or lex == "mod" or lex == "and"):
        next()
        factor()


#method for factors
def factor():
    if(lex == "-" or lex == "not"):
        next()
    if(lex == "false" or lex == "true" or nToken == INT):
        literal()
    elif(nToken == IDENTIFIER):
        next()
    elif(lex == "("):
        next()
        expression()
        match(")")
    else:
        expected(["false","true",INT,IDENTIFIER,"("])

#method for literal
def literal():
    assert(lex == "true" or lex == "false" or nToken  == INT), "Error found at "+str(row)+":"+str(column)+ " should be 'true','false', or an INT"
    if(nToken == INT):
        next()
    else:
        booleanliteral()

#method for boolean literal statement
def booleanliteral():
    next()

#method for Iterative Statement
def iterative():
    match("while")
    expression()
    match("do")
    body()
    match("end")

#method for print
def printStatement():
    match("print")
    expression()

#AST METHODS
#Method for an AST with 3 children
def threeTree(root, child1, child2, child3):
    print(root)
    print("    "+str(child1))
    print("    " + str(child2))
    print("    "+str(child3))

##Method for a AST with one child, examples being: bool or int
def oneTree(root, child1,ctr):
    s = (str(root)+'\n'+"    "*ctr+str(child1))
    return s
#Method for an AST node with 2 children
def twoTree(root, child1, child2, ctr):
    s = (str(root)+'\n'+"    "*ctr+str(child1)+'\n'+"    "*ctr+str(child2))
    return s


#Calling Main
main()

