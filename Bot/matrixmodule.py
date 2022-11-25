import numpy as np 

def mathInputEvaluate(args):
    arglen = len(args)
    if arglen <= 1:
        return "Bitte gebe weitere Argumente an"
    formattedInputList = [None]*arglen
    for i in range(arglen):
        try:
            formattedInputList[i] = formatInput(args[i])
        except:
            return "Formatierungsfehler"
    return eval(formattedInputList)
    
def printvals(elementList):
    for i in range(len(elementList)):
        print(elementList[i].value)

def eval(elementList):
    if len(elementList) == 1:
        return elementList[0].value
    # bracket evaluation
    brackEval = bracketEvaluation(elementList)
    if brackEval != None:
        return brackEval
    # multiplication evaluation
    multEval = multEvaluation(elementList)
    if multEval != None:
        return multEval
    # addition and subtraction evaluation
    addsubEval = addsubEvaluation(elementList)
    if addsubEval.any() != None:
        return addsubEval

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
        bracketEval = eval(elementList[firstbracketIndex+1:secondbracketIndex])
        beforeBrack = elementList[0:firstbracketIndex]
        afterBrack = []
        # check if second bracket is last element
        if secondbracketIndex != len(elementList)-1:
            afterBrack = elementList[secondbracketIndex+1:len(elementList)]
        else:
            afterBrack = []
        res = elementsJoin(beforeBrack,bracketEval,afterBrack)
        return eval(res)
    return None
            
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
            return eval(res)
    return None

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
                        addEval = elementList[i-1].value + elementList[i+1].value
                    except:
                        raise MatrixAdditionError
                    res = elementsJoin(beforeOp,addEval,afterOp)
                    return eval(res)
                case "-":
                    try:
                        subEval = elementList[i-1].value - elementList[i+1].value
                    except:
                        raise MatrixSubtractionError
                    res = elementsJoin(beforeOp,subEval,afterOp)
                    return eval(res)

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
    res.append(Element(matrix,"Matrix","None"))
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
                return Element(np.matrix(matString),"matrix","None")
            except:
                raise MatrixParseError

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