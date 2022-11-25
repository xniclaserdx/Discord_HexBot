import numpy as np 

def mathInputEvaluate(args):
    arglen = len(args)
    if arglen <= 1:
        error("not enough arguments")
        return returnError()
    formattedInputList = [None]*arglen
    for i in range(arglen):
        try:
            formattedInputList[i] = formatInput(args[i])
        except:
            return "Fehler du Trollo"
    return eval(formattedInputList)
    
def printvals(elementList):
    for i in range(len(elementList)):
        print(elementList[i].value)

def eval(elementList):
    if len(elementList) == 1:
        return elementList[0].value
    # bracket evaluation
    firstbracketIndex = -1
    secondbracketIndex = -1
    openBracketCount = 0
    maxBracketCount = 0
    for i in range(len(elementList)):
        if elementList[i].type == "bracket" and elementList[i].value == "(":
            openBracketCount += 1
            if openBracketCount > maxBracketCount:
                maxBracketCount = openBracketCount
                firstbracketIndex = i
        elif elementList[i].type == "bracket" and elementList[i].value == ")":
            openBracketCount -= 1
            if openBracketCount < 0:
                raise BracketMismatchError
            if secondbracketIndex < firstbracketIndex:
                secondbracketIndex = i
    if openBracketCount != 0:
        raise BracketMismatchError
    if firstbracketIndex != -1:
        if firstbracketIndex + 1 == secondbracketIndex:
            raise EmptyBracketsError
        bracketEval = eval(elementList[firstbracketIndex+1:secondbracketIndex])
        beforeBrack = elementList[0:firstbracketIndex]
        afterBrack = []
        if secondbracketIndex != len(elementList)-1:
            afterBrack = elementList[secondbracketIndex+1:len(elementList)]
        else:
            afterBrack = []
        toEval = beforeBrack
        toEval.append(Element(bracketEval,"matrix","None"))
        toEval.extend(afterBrack)
        return eval(toEval)
    # multiplication evaluation
    for i in range(len(elementList)):
        if elementList[i].type == "operator" and elementList[i].value == "*":
            if i == 0 or i == len(elementList) or elementList[i-1].type != "matrix" or elementList[i+1].type != "matrix":
                raise MultiplicationOperandError
            beforeMult = elementList[0:i-1]
            afterMult = []
            if i+1 == len(elementList):
                afterMult = []
            else:
                afterMult = elementList[i+2:len(elementList)]
            try:
                multEval = np.matmul(elementList[i-1].value,elementList[i+1].value)
            except:
                raise MatrixMultiplicationError
            toEval = beforeMult
            toEval.append(Element(multEval,"matrix","None"))
            toEval.extend(afterMult)
            return eval(toEval)
    for i in range(len(elementList)):
        if elementList[i].type == "operator" and (elementList[i].value == "+" or elementList[i].value == "-"):
            if i == 0 or i == len(elementList) or elementList[i-1].type != "matrix" or elementList[i+1].type != "matrix":
                match elementList[i].value:
                    case "+":
                        raise AdditionOperandError
                    case "-":
                        raise SubtractionOperandError
            beforeOp = elementList[0:i-1]
            afterOp = []
            if i+1 == len(elementList):
                afterOp = []
            else:
                afterOp = elementList[i+2:len(elementList)]
            match elementList[i].value:
                case "+":
                    # hier funktioniert was
                    try:
                        addEval = elementList[i-1].value + elementList[i+1].value
                    except:
                        raise MatrixAdditionError
                    toEval = beforeOp
                    toEval.append(Element(addEval,"matrix","None"))
                    toEval.extend(afterOp)
                    return eval(toEval)
                case "-":
                    try:
                        subEval = elementList[i-1].value - elementList[i+1].value
                    except:
                        raise MatrixSubtractionError
                    toEval = beforeOp
                    toEval.append(Element(subEval,"matrix","None"))
                    toEval.extend(afterOp)
                    return eval(toEval)

            



def toMatrix(string):
    matrStr = textMatrixFormat(string)
    try:
        return np.matrix(matrStr)
    except:
        raise MatrixParseError
     
def formatInput(input):
    match input:
        case "+":
            return Element("+","operator","None")
        case "-":
            return Element("-","operator","None")
        case "*":
            return Element("*","operator","None")
        case "(":
            return Element("(","bracket","None")
        case ")":
            return Element(")","bracket","None")
        case _:
            matString = textMatrixFormat(input)
            #try: 
            return Element(np.matrix(matString),"matrix","None")
            #except:
            #    raise MatrixParseError

# changes user input to allow conversion into a matrix
def textMatrixFormat(input):
    return input.replace(',',' ')

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

# final error String to be returned
def returnError():
    return "MathModuleError: "+errorStr

# class for formatting user input to differentiate between operators, matrices etc.
class Element(object):
    def __init__(self,value,type,description):
        self.value = value
        self.type = type
        self.description = description
    
        
# error classes    
class MatrixParseError:
    pass

class BracketMismatchError:
    pass

class EmptyBracketsError:
    pass

class MultiplicationOperandError:
    pass
    
class MatrixMultiplicationError:
    pass

class AdditionOperandError:
    pass

class MatrixAdditionError:
    pass

class SubtractionOperandError:
    pass
    
class MatrixSubtractionError:
    pass
