PLUS, EOF, MINUS, IDENTIFIER, ASSIGN, MUL, DIVIDE, DIV, MOD, KEYWORD = 'PLUS', 'EOF', 'MINUS', 'IDENTIFIER', 'ASSIGN', 'MULTIPLY', 'DIVIDE', 'DIV', 'MOD', 'KEYWORD'

# Removed DATATYPE dictionary and replaced with individual variables
INTEGER = 'INTEGER'
REAL = 'REAL'
STRING = 'STRING'

KEYWORDS = ['OUTPUT', 'INPUT', 'IF', 'THEN', 'ELSE', 'ENDIF', 
            'WHILE', 'DO', 'ENDWHILE', 'REPEAT', 'UNTIL', 
            'FOR', 'TO', 'NEXT', 'FUNCTION', 'PROCEDURE', 
            'RETURNS', 'ENDFUNCTION', 'ENDPROCEDURE', 'TRUE', 'FALSE']

OPERATORS = [MINUS, PLUS, MUL, DIVIDE, MOD, DIV]


class Token(object):
    
    def __init__(self, type, value):
        self.type = type
        self.value = value 

    def __str__(self):
        return 'Token({type},{value})'.format(
            type = self.type,
            value = repr(self.value)
        )
    

class Lexer():

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.list = []
        self.current_char = self.text[self.pos] if len(self.text) > 0 else None
        
    def error(self):
        raise Exception('Error parsing input')
    
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()
        
    def integer(self):
        result = ""
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
    
    def word(self):
        result = ""
        while self.current_char and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        return result

    def tokenize(self):
        list_index = 0
        while True:
            self.list.append(self.get_next_token())
            if self.list[list_index].type == EOF:
                break
            list_index += 1

    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            elif self.current_char.isdigit():    
                number = self.integer()
                return Token(INTEGER, number)
            
            elif self.current_char.isalpha():
                word = self.word()
                if word in KEYWORDS:
                    return Token(KEYWORD, word)
                return Token(IDENTIFIER, word)
            
            elif self.current_char == "+":
                self.advance()
                return Token(PLUS, '+')
            
            elif self.current_char == "<":
                nextChar1 = self.text[self.pos+1]
                if nextChar1 == "-":
                    nextChar2 = self.text[self.pos+2]
                    if nextChar2 == "-":
                        self.advance()
                        self.advance()
                        self.advance()
                        return Token(ASSIGN, '<--')
            
            elif self.current_char == "-":
                self.advance()
                return Token(MINUS, '-')
            
            else:
                self.error()

        return Token(EOF, None)
    
class varNode():
    def __init__(self, name):
        self.name = name

class numNode():
    def __init__(self, num):
        self.num = num

class BinOpNode():
    def __init__(self, operation, left, right):
        self.opr = operation
        self.left = left
        self.right = right

class AssignNode():
    def __init__(self, name, expression):
        self.name = name
        self.expr = expression


class Parser():
    def __init__(self, list):
        self.tokenList = list
        self.pos = 0

    def eat(self, expected_type):
        if self.tokenList[self.pos].type == expected_type:
            self.pos += 1
        else:
            raise SyntaxError()
    
    def expression(self):
        if self.tokenList[self.pos].type == IDENTIFIER:
            left_tree = varNode(self.tokenList[self.pos].value)
            self.eat(IDENTIFIER)

        elif self.tokenList[self.pos].type == INTEGER:  
            left_tree = numNode(self.tokenList[self.pos].value)
            self.eat(INTEGER)                           

        while self.tokenList[self.pos].type in OPERATORS:
            operator = self.tokenList[self.pos].type 
            self.eat(operator)
            if self.tokenList[self.pos].type == IDENTIFIER:
                right_tree = varNode(self.tokenList[self.pos].value)
                self.eat(IDENTIFIER)
            elif self.tokenList[self.pos].type == INTEGER:  
                right_tree = numNode(self.tokenList[self.pos].value)
                self.eat(INTEGER)                           
            else:
                raise SyntaxError()
            
            left_tree = BinOpNode(operator, left_tree, right_tree)
        
        return left_tree
    
    def assignment(self):
        if self.tokenList[self.pos].type == IDENTIFIER:
            name = self.tokenList[self.pos].value
            self.eat(IDENTIFIER)
            if self.tokenList[self.pos].type == ASSIGN:
                 self.eat(ASSIGN)
                 left_tree = self.expression()
            else:
                raise SyntaxError()
            
        return AssignNode(name, left_tree)

    def parse(self):
        if self.tokenList[self.pos].type == EOF:
            return None
        
        if (self.pos + 1 < len(self.tokenList) and self.tokenList[self.pos].type == IDENTIFIER and self.tokenList[self.pos + 1].type == ASSIGN):
            node = self.assignment()

        else:
            node = self.expression()


        self.eat(EOF)
        return node
     
       
        


class Interpreter():

    def __init__(self, root):
        self.ast = root
        self.variables = {}
       
    def visit(self, node):
        if isinstance(node, numNode):
            return node.num
        
        elif isinstance(node, varNode):
            return self.variables[node.name]

        elif isinstance(node, AssignNode):
            value = self.visit(node.expr)
            self.variables[node.name] = value
            return value

        else:
            left = self.visit(node.left)
            right = self.visit(node.right)
            if node.opr == PLUS:
                output = left + right
            elif node.opr == MINUS:
                output = left - right
            
        return output
            
    def evaluate(self):
        return self.visit(self.ast)
    
# ==================================================
# TEST RUNNER FOR YOUR INTERPRETER
# ==================================================

def run_test(input_string):
    """Runs the full pipeline on a single input string."""
    print(f'Input: "{input_string}"')
    try:
        # 1. Lexer
        lexer = Lexer(input_string)
        lexer.tokenize()
        # Uncomment the line below to see the token list for debugging
        # print(f"  Tokens: {lexer.list}")

        # 2. Parser
        parser = Parser(lexer.list)
        ast_root = parser.parse()
        
        if ast_root is None:
            print("  Result: (Empty input)")
            return

        # 3. Interpreter
        interpreter = Interpreter(ast_root)
        result = interpreter.evaluate()
        
        print(f"  Result: {result}")
        print(f"  Variables: {interpreter.variables}")
        
    except SyntaxError as e:
        print(f"  Syntax Error: {e}")
    except KeyError as e:
        print(f"  Runtime Error: Undefined variable {e}")
    except Exception as e:
        print(f"  Unexpected Error: {e}")
    print("-" * 40)


# -------- RUN THE TESTS --------
print("========== INTERPRETER TEST SUITE ==========\n")

test_cases = [
    # --- Basic Expressions ---
    "3 + 4",                 # Expected: 7
    "42",                    # Expected: 42
    "10 + 20 - 5",          # Expected: 25 (left-to-right: (10+20)-5)

    # --- Variable Assignments ---
    "x <-- 10",               # Expected: None (stores x=10)
    "x <-- 3 + 4",            # Expected: None (stores x=7)

    # --- Variable Lookup (Will raise error because fresh interpreter) ---
    "x + 2",                # Expected: Runtime Error (undefined variable)
    
    # --- Invalid Syntax ---
    "3 +",                  # Expected: Syntax Error
    
    # --- Empty Input ---
    "",                     # Expected: (Empty input)
]

print("--- Testing individual statements (fresh interpreter each time) ---")
for test in test_cases:
    run_test(test)

print("========== TESTS COMPLETE ==========")