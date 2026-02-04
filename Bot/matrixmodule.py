"""Module for matrix calculations with LaTeX rendering."""
import numpy as np
import texmodule
import interactions
from interactions.ext.files import command_send
import io


async def math_input_evaluate(args: list) -> bytes:
    """
    Evaluate a mathematical expression and return rendered LaTeX image.
    
    Args:
        args: List of expression components (matrices, operators, brackets)
        
    Returns:
        BytesIO containing the rendered PNG image
    """
    arg_len = len(args)
    formatted_input_list = [None] * arg_len
    
    for i in range(arg_len):
        try:
            formatted_input_list[i] = format_input(args[i])
        except Exception:
            # Formatting error
            error_msg = "Invalid matrix format. Expected format: (1,2;3,4) with spaces between elements"
            return await texmodule.texToPng(tex_err_out(error_msg))
    
    tex_string = tex_out(
        element_list_to_tex(formatted_input_list),
        matrix_to_tex(evaluate_expression(formatted_input_list).value)
    )
    return await texmodule.texToPng(tex_string)


def element_list_to_tex(element_list: list) -> str:
    """
    Convert a list of elements to LaTeX string.
    
    Args:
        element_list: List of Element objects
        
    Returns:
        LaTeX string representation
    """
    tex_string = ''
    for element in element_list:
        if element.type == 'bracket':
            tex_string += element.value
        elif element.type == 'operator':
            if element.value == '+':
                tex_string += '+'
            elif element.value == '-':
                tex_string += '-'
            elif element.value == 'X':
                tex_string += r'\cdot '
        elif element.type == 'matrix':
            tex_string += matrix_to_tex(element.value)
    return tex_string


def matrix_to_tex(matrix: np.ndarray) -> str:
    """
    Convert a numpy matrix to LaTeX string representation.
    
    Args:
        matrix: Numpy array to convert
        
    Returns:
        LaTeX string for the matrix
    """
    rows, cols = matrix.shape
    mat_tex_beg = r'\left(\begin{array}{' + cols * 'c' + '}'
    mat_tex_end = r'\end{array}\right)'
    mat_tex_mid = ''
    
    for i in range(rows):
        for j in range(cols):
            if j == 0 and j != cols - 1:
                mat_tex_mid += str(get_mat_item(matrix, (i, j)))
            elif j == 0 and j == cols - 1:
                mat_tex_mid += str(get_mat_item(matrix, (i, j))) + r'\\'
            elif j == cols - 1:
                mat_tex_mid += r'&' + str(get_mat_item(matrix, (i, j))) + r'\\'
            else:
                mat_tex_mid += r'&' + str(get_mat_item(matrix, (i, j)))
    
    return mat_tex_beg + mat_tex_mid + mat_tex_end


def get_mat_item(matrix: np.ndarray, position: tuple) -> float:
    """
    Get matrix item at position, returning int if whole number.
    
    Args:
        matrix: Numpy array
        position: Tuple (row, col)
        
    Returns:
        Integer or float value
    """
    value = matrix.item(position)
    if int(value) == value:
        return int(value)
    return value


def tex_out(input_: str, output: str) -> str:
    """
    Create complete LaTeX document string for rendering.
    
    Args:
        input_: LaTeX string for input expression
        output: LaTeX string for result
        
    Returns:
        Complete LaTeX document
    """
    latex_start = r'\documentclass{article}\begin{document}\thispagestyle{empty}$'
    latex_mid = r'\\~\\ = '
    latex_end = r'$\end{document}'
    return latex_start + input_ + latex_mid + output + latex_end


def tex_err_out(error: str) -> str:
    """
    Create LaTeX document for error message.
    
    Args:
        error: Error message to display
        
    Returns:
        LaTeX document with error
    """
    latex_start = r'\documentclass{article}\begin{document}\thispagestyle{empty}Error: '
    latex_end = r'\end{document}'
    return latex_start + error + latex_end
        

def evaluate_expression(element_list: list):
    """
    Evaluate a mathematical expression represented as a list of elements.
    
    Args:
        element_list: List of Element objects representing the expression
        
    Returns:
        Element object with the result
    """
    if len(element_list) == 1:
        return element_list[0]
    # bracket evaluation
    brack_eval = bracket_evaluation(element_list)
    if brack_eval[1]:
        return brack_eval[0]
    # multiplication evaluation
    mult_eval = mult_evaluation(element_list)
    if mult_eval[1]:
        return mult_eval[0]
    # addition and subtraction evaluation
    addsub_eval = addsub_evaluation(element_list)
    if addsub_eval[1]:
        return addsub_eval[0]
    return element_list[0]

# bracketEvaluation     
def bracket_evaluation(element_list: list) -> tuple:
    """
    Evaluate expressions within brackets.
    
    Args:
        element_list: List of Element objects
        
    Returns:
        Tuple (result, success_flag)
    """
    first_bracket_index = -1
    second_bracket_index = -1
    open_bracket_count = 0
    max_bracket_count = 0
    for i in range(len(element_list)):
        if element_list[i].type == "bracket" and element_list[i].value == "(":
            open_bracket_count += 1
            # find innermost opening bracket
            if open_bracket_count > max_bracket_count:
                max_bracket_count = open_bracket_count
                first_bracket_index = i
        elif element_list[i].type == "bracket" and element_list[i].value == ")":
            open_bracket_count -= 1
            # too many closed brackets
            if open_bracket_count < 0:
                raise BracketMismatchError
            # search for the first closing bracket after the most innermost opening one
            if second_bracket_index < first_bracket_index:
                second_bracket_index = i
    # too many open brackets
    if open_bracket_count != 0:
        raise BracketMismatchError
    # brackets found
    if first_bracket_index != -1:
        if first_bracket_index + 1 == second_bracket_index:
            raise EmptyBracketsError
        bracket_eval = evaluate_expression(element_list[first_bracket_index+1:second_bracket_index]).value
        before_brack = element_list[0:first_bracket_index]
        after_brack = []
        # check if second bracket is last element
        if second_bracket_index != len(element_list)-1:
            after_brack = element_list[second_bracket_index+1:len(element_list)]
        else:
            after_brack = []
        res = elements_join(before_brack, bracket_eval, after_brack)
        return evaluate_expression(res), True
    return None, False
            
# evaluate multiplication
def mult_evaluation(element_list: list) -> tuple:
    """
    Evaluate multiplication operations.
    
    Args:
        element_list: List of Element objects
        
    Returns:
        Tuple (result, success_flag)
    """
    for i in range(len(element_list)):
        if element_list[i].type == "operator" and element_list[i].value == "X":
            if not valid_binary_op_position(element_list, i):
                raise MultiplicationOperandError
            before_mult, after_mult = split_element_list_for_binary_op(element_list, i)
            try:
                mult_eval = np.matmul(element_list[i-1].value, element_list[i+1].value)
            except ValueError:
                raise MatrixMultiplicationError("Matrix dimensions incompatible for multiplication")
            res = elements_join(before_mult, mult_eval, after_mult)
            return evaluate_expression(res), True
    return None, False

# evaluate addition and subtraction
def addsub_evaluation(element_list: list) -> tuple:
    """
    Evaluate addition and subtraction operations.
    
    Args:
        element_list: List of Element objects
        
    Returns:
        Tuple (result, success_flag)
    """
    for i in range(len(element_list)):
        if element_list[i].type == "operator" and (element_list[i].value == "+" or element_list[i].value == "-"):
            if not valid_binary_op_position(element_list, i):
                if element_list[i].value == "+":
                    raise AdditionOperandError
                else:
                    raise SubtractionOperandError
            before_op, after_op = split_element_list_for_binary_op(element_list, i)
            if element_list[i].value == "+":
                try:
                    add_eval = np.add(element_list[i-1].value, element_list[i+1].value)
                except ValueError:
                    raise MatrixAdditionError("Matrix dimensions must match for addition")
                res = elements_join(before_op, add_eval, after_op)
                return evaluate_expression(res), True
            else:  # subtraction
                try:
                    sub_eval = np.subtract(element_list[i-1].value, element_list[i+1].value)
                except ValueError:
                    raise MatrixSubtractionError("Matrix dimensions must match for subtraction")
                res = elements_join(before_op, sub_eval, after_op)
                return evaluate_expression(res), True
    return None, False


def valid_binary_op_position(element_list: list, i: int) -> bool:
    """
    Check if binary operator is in valid position.
    
    Args:
        element_list: List of Element objects
        i: Index of operator
        
    Returns:
        True if valid, False otherwise
    """
    if (i == 0 or i + 1 == len(element_list) or 
        element_list[i - 1].type != "matrix" or 
        element_list[i + 1].type != "matrix"):
        return False
    return True


def split_element_list_for_binary_op(element_list: list, i: int) -> tuple:
    """
    Split element list around a binary operator.
    
    Args:
        element_list: List of Element objects
        i: Index of operator
        
    Returns:
        Tuple (before_op, after_op)
    """
    before_op = element_list[0:i - 1]
    
    # Check if there are elements left to the right of the binary operation
    if i + 2 == len(element_list):
        after_op = []
    else:
        after_op = element_list[i + 2:len(element_list)]
    
    return before_op, after_op


def to_matrix(string: str) -> np.ndarray:
    """
    Convert a string to a numpy matrix.
    
    Args:
        string: String representation of matrix
        
    Returns:
        Numpy matrix
    """
    matr_str = text_matrix_format(string)
    try:
        return np.matrix(matr_str)
    except ValueError:
        raise MatrixParseError

    
def elements_join(list1: list, matrix: np.ndarray, list2: list) -> list:
    """
    Join two lists with a matrix element in between.
    
    Args:
        list1: First list
        matrix: Matrix to insert
        list2: Second list
        
    Returns:
        Combined list
    """
    res = list1
    res.append(Element(matrix, "matrix", "None"))
    res.extend(list2)
    return res

     
def format_input(input_str: str):
    """
    Format user input string into an Element object.
    
    Args:
        input_str: Input string (operator, bracket, or matrix)
        
    Returns:
        Element object
    """
    if input_str == "+":
        return Element("+", "operator", "None")
    elif input_str == "-":
        return Element("-", "operator", "None")
    elif input_str == "X":
        return Element("X", "operator", "None")
    elif input_str == "(":
        return Element("(", "bracket", "None")
    elif input_str == ")":
        return Element(")", "bracket", "None")
    else:
        mat_string = text_matrix_format(input_str)
        try: 
            mat_rows = mat_string.split(";")
            mat_rows = list(map(lambda x: x.split(" "), mat_rows))
            for r, row in enumerate(mat_rows):
                for c, element in enumerate(row):
                    mat_rows[r][c] = float(element)
            return Element(np.array(mat_rows), "matrix", "None")
        except (ValueError, IndexError):
            raise MatrixParseError


def text_matrix_format(input_str: str) -> str:
    """
    Convert user input to matrix format.
    
    Args:
        input_str: User input string
        
    Returns:
        Formatted string for matrix conversion
    """
    return input_str.replace(',', ' ')[1:-1]



# class for formatting user input to differentiate between operators, matrices etc.
class Element:
    """Represents an element in a mathematical expression."""
    
    def __init__(self, value, ptype: str, description: str):
        """
        Initialize an Element.
        
        Args:
            value: The value of the element (matrix, operator, or bracket)
            ptype: Type of element ('matrix', 'operator', 'bracket')
            description: Description of the element
        """
        self.value = value
        self.type = ptype
        self.description = description


# Error classes    
class MatrixParseError(Exception):
    """Raised when matrix parsing fails."""
    pass


class BracketMismatchError(Exception):
    """Raised when brackets don't match."""
    pass


class EmptyBracketsError(Exception):
    """Raised when empty brackets are found."""
    pass


class MultiplicationOperandError(Exception):
    """Raised when multiplication has invalid operands."""
    pass

    
class MatrixMultiplicationError(Exception):
    """Raised when matrix multiplication fails."""
    pass


class AdditionOperandError(Exception):
    """Raised when addition has invalid operands."""
    pass


class MatrixAdditionError(Exception):
    """Raised when matrix addition fails."""
    pass



class SubtractionOperandError(Exception):
    """Raised when subtraction has invalid operands."""
    pass

    
class MatrixSubtractionError(Exception):
    """Raised when matrix subtraction fails."""
    pass


class MatrixModule(interactions.Extension):
    """Extension module for matrix calculation commands."""
    
    def __init__(self, client):
        self.client = client
    
    @interactions.extension_command(
        name="hex_matrix",
        description="Can perform multiple matrix operations",
        options=[
            interactions.Option(
                name="expression",
                description="expression to be evaluated, matrix format: (1,2;3,4), spaces between inputs needed",
                type=interactions.OptionType.STRING,
                required=True
            )
        ]
    )
    async def matrix_command(self, ctx: interactions.CommandContext, expression: str):
        """Handle matrix calculation command."""
        expression_args = expression.split(" ")
        image = await math_input_evaluate(expression_args)
        image_byte_arr = io.BytesIO()
        image.save(image_byte_arr, format='PNG')
        image_byte_arr.seek(0)
        await command_send(ctx, "", files=interactions.File(fp=image_byte_arr, filename="response.png"))


def setup(client):
    """Set up the MatrixModule extension."""
    MatrixModule(client)