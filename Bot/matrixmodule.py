import numpy as np
import texmodule
import interactions
from interactions.ext.files import command_send
import io

async def mathInputEvaluate(args):
    # return await texmodule.texToPng(r'\documentclass{article}\usepackage{xcolor}\begin{document}\thispagestyle{empty}$\frac{3}{2} \cdot \frac{2}{3} = 1$ \end{document}')
    arglen = len(args)
    formattedInputList = [None]*arglen
    for i in range(arglen):
        try:
            formattedInputList[i] = formatInput(args[i])
        except:
            # Formatierungsfehler
            return await texmodule.texToPng(texErrOut)
    texString = texOut(elementListtoTex(formattedInputList),matrixToTex(eval(formattedInputList).value))
    return await texmodule.texToPng(texString)
    
def printvals(elementList):
    for i in range(len(elementList)):
        print(elementList[i].value)

def elementListtoTex(elementList):
    texString = ''
    for i in elementList:
        if i.type == 'bracket':
            texString += i.value
        elif i.type == 'operator':
            match i.value:
                case '+':
                    texString += '+'
                case '-':
                    texString += '-'
                case 'X':
                    texString += r'\cdot '
        elif i.type == 'matrix':
            texString += matrixToTex(i.value)
    return texString

def matrixToTex(matrix):
    rows, cols = matrix.shape
    matTexBeg = r'\left(\begin{array}{'+cols*'c'+'}'
    matTexEnd = r'\end{array}\right)'
    matTexMid = ''
    for i in range(rows):
        for j in range(cols):
            if j == 0:
                matTexMid += str(matrix.item((i,j)))
            elif j == cols-1:
                matTexMid += r'&'+ str(matrix.item((i,j)))+r'\\'
            else:
                matTexMid += r'&'+ str(matrix.item((i,j)))
    return matTexBeg+matTexMid+matTexEnd

def texOut(input_,output):
    latexStart = r'\documentclass{article}\begin{document}\thispagestyle{empty}$'
    latexMid = r'\\~\\ = '
    latexEnd = r'$\end{document}'
    return latexStart + input_ + latexMid + output + latexEnd

def texErrOut(error):
    # error muss hier noch verwendet werden (zu implementieren)
    latexStart = r'\documentclass{article}\begin{document}\thispagestyle{empty}Fehler'
    latexEnd = r'\end{document}'
    return latexStart + latexEnd
        

def eval(elementList):
    if len(elementList) == 1:
        return elementList[0]
    # bracket evaluation
    brackEval = bracketEvaluation(elementList)
    if brackEval[1]:
        return brackEval[0]
    # multiplication evaluation
    multEval = multEvaluation(elementList)
    if multEval[1]:
        return multEval[0]
    # addition and subtraction evaluation
    addsubEval = addsubEvaluation(elementList)
    if addsubEval[1]:
        return addsubEval[0]

# bracketEvaluation     
def bracketEvaluation(elementList):
    firstbracketIndex = -1
    secondbracketIndex = -1
    openBracketCount = 0
    maxBracketCount = 0
    for i in range(len(elementList)):
        if elementList[i].type == "bracket" and elementList[i].value == "(":
            openBracketCount += 1
            # find innermost opening bracket
            if openBracketCount > maxBracketCount:
                maxBracketCount = openBracketCount
                firstbracketIndex = i
        elif elementList[i].type == "bracket" and elementList[i].value == ")":
            openBracketCount -= 1
            # too many closed brackets
            if openBracketCount < 0:
                raise BracketMismatchError
            # search for the first closing bracket after the most innermost opening one
            if secondbracketIndex < firstbracketIndex:
                secondbracketIndex = i
    # too many open brackets
    if openBracketCount != 0:
        raise BracketMismatchError
    # brackets found
    if firstbracketIndex != -1:
        if firstbracketIndex + 1 == secondbracketIndex:
            raise EmptyBracketsError
        bracketEval = eval(elementList[firstbracketIndex+1:secondbracketIndex]).value
        beforeBrack = elementList[0:firstbracketIndex]
        afterBrack = []
        # check if second bracket is last element
        if secondbracketIndex != len(elementList)-1:
            afterBrack = elementList[secondbracketIndex+1:len(elementList)]
        else:
            afterBrack = []
        res = elementsJoin(beforeBrack,bracketEval,afterBrack)
        return eval(res), True
    return None, False
            
# evaluate multiplication
def multEvaluation(elementList):
    for i in range(len(elementList)):
        if elementList[i].type == "operator" and elementList[i].value == "X":
            if not validBinaryOpPosition(elementList,i):
                raise MultiplicationOperandError
            beforeMult, afterMult = splitElementListForBinaryOp(elementList,i)
            try:
                multEval = np.matmul(elementList[i-1].value,elementList[i+1].value)
            except:
                raise MatrixMultiplicationError
            res = elementsJoin(beforeMult,multEval,afterMult)
            return eval(res), True
    return None, False

# evaluate addition and subtraction
def addsubEvaluation(elementList):
    for i in range(len(elementList)):
        if elementList[i].type == "operator" and (elementList[i].value == "+" or elementList[i].value == "-"):
            if not validBinaryOpPosition(elementList,i):
                match elementList[i].value:
                    case "+":
                        raise AdditionOperandError
                    case "-":
                        raise SubtractionOperandError
            beforeOp, afterOp = splitElementListForBinaryOp(elementList,i)
            match elementList[i].value:
                case "+":
                    try:
                        addEval = np.add(elementList[i-1].value,elementList[i+1].value)
                    except:
                        raise MatrixAdditionError
                    res = elementsJoin(beforeOp,addEval,afterOp)
                    return eval(res), True
                case "-":
                    try:
                        subEval = np.subtract(elementList[i-1].value,elementList[i+1].value)
                    except:
                        raise MatrixSubtractionError
                    res = elementsJoin(beforeOp,subEval,afterOp)
                    return eval(res), True
    return None, False

def validBinaryOpPosition(elementList,i):
    if i == 0 or i+1 == len(elementList) or elementList[i-1].type != "matrix" or elementList[i+1].type != "matrix":
        return False
    else:
        return True
                
def splitElementListForBinaryOp(elementList,i):
    beforeOp = elementList[0:i-1]
    afterOp = []
    # check if there are elements left to the right of the binary operation
    if i+2 == len(elementList):
        afterOp = []
    else:
        afterOp = elementList[i+2:len(elementList)]
    return beforeOp, afterOp

def toMatrix(string):
    matrStr = textMatrixFormat(string)
    try:
        return np.matrix(matrStr)
    except:
        raise MatrixParseError
    
def elementsJoin(list1,matrix,list2):
    res = list1
    res.append(Element(matrix,"matrix","None"))
    res.extend(list2)
    return res

     
def formatInput(input):
    match input:
        case "+":
            return Element("+","operator","None")
        case "-":
            return Element("-","operator","None")
        case "X":
            return Element("X","operator","None")
        case "(":
            return Element("(","bracket","None")
        case ")":
            return Element(")","bracket","None")
        case _:
            matString = textMatrixFormat(input)
            try: 
                mat_rows = matString.split(";")
                mat_rows = list(map(lambda x: x.split(" "),mat_rows))
                for r,row in enumerate(mat_rows):
                    for c,element in enumerate(row):
                        mat_rows[r][c] = int(element)
                return Element(np.array(mat_rows),"matrix","None")
            except:
                raise MatrixParseError

# changes user input to allow conversion into a matrix
def textMatrixFormat(input):
    return input.replace(',',' ')[1:-1]

# determine whether the input can be interpreted as a matrix of numeric values or if it has to be treated as string matrix
def matrixType(matrix):
    type = "num"
    if matrix.ndim == "1":
        for i in matrix:
            try:
                float(matrix[i])
            except:
                type = "str"
    else:
        type = "num"
        for i in matrix.shape[0]:
            for j in matrix.shape[1]:
                try:
                    float(matrix[i][j])
                except:
                    type = "str"
    return type

# class for formatting user input to differentiate between operators, matrices etc.
class Element(object):
    def __init__(self,value,ptype,description):
        self.value = value
        self.type = ptype
        self.description = description



# error classes    
class MatrixParseError(Exception):
    pass

class BracketMismatchError(Exception):
    pass

class EmptyBracketsError(Exception):
    pass

class MultiplicationOperandError(Exception):
    pass
    
class MatrixMultiplicationError(Exception):
    pass

class AdditionOperandError(Exception):
    pass

class MatrixAdditionError(Exception):
    pass

class SubtractionOperandError(Exception):
    pass
    
class MatrixSubtractionError(Exception):
    pass

class MatrixModule(interactions.Extension):
    def __init__(self,client):
        self.client = client
    
    # command for matrix calculations
    @interactions.extension_command(
        name = "hex_matrix",
        description = "Can perfom multiple matrix operations",
        options = [
            interactions.Option(
                name = "expression",
                description = "expression to be evaluated, matrix format: (1,2;3,4), spaces between inputs needed",
                type = interactions.OptionType.STRING,
                required = True
            )
        ]
    )
    async def matrix_command(self,ctx: interactions.CommandContext, expression: str):
        expression_args = expression.split(" ")
        image = await mathInputEvaluate(expression_args)
        imageByteArr = io.BytesIO()
        image.save(imageByteArr,format='PNG')
        imageByteArr.seek(0)
        await command_send(ctx,"",files = interactions.File(fp = imageByteArr,filename="response.png"))


def setup(client):
    MatrixModule(client)