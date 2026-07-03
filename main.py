INTEGER , PLUS , EOF , MINUS ,IDENTIFIER,ASSIGN ,OUTPUT= 'INTEGER','PLUS','EOF' ,'MINUS','IDENTIFIER','ASSIGN','OUTPUT'
OPERATORS = [MINUS,PLUS]
class Token(object):
    
    def __init__(self,type,value):
        self.type = type
        self.value = value 

    def __str__(self):
        
        return 'Token({type},{value})'.format(
            type = self.type,
            value = repr(self.value)
        )
    

class Lexer():

    def __init__(self,text):
        
        self.text = text
        self.pos = 0
        self.list = []
        self.current_char = self.text[self.pos] if len(self.text) > 0 else None
    def error(self):
        raise Exception('Error parsing input')
    
    def advance(self):

        self.pos += 1
       

        if self.pos > len(self.text) -1:
            self.current_char =  None
        else:

            self.current_char = self.text[self.pos]

    
    def skip_whitespace(self):
        
        while self.current_char and self.current_char.isspace() :
            self.advance()
        
    def integer(self):
        result = ""

        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return int(result)
    
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
                return Token('INTEGER',number)

            elif self.current_char == "+":
                self.advance()
                return Token("PLUS",'+')
            
            elif self.current_char == "-":
                self.advance()
                return Token("MINUS",'-')
            
            else:
                self.error()

        return Token(EOF, None)
    
class numNode():
    def __init__(self,num):
        self.num = num

class BinOpNode():
    def __init__(self,operation,left,right):
        self.opr = operation
        self.left = left
        self.right = right

class Parser():
    def __init__(self,list):
        self.tokenList = list
        self.pos = 0

    
    def eat(self,expected_type):
        if self.tokenList[self.pos].type == expected_type:
            self.pos += 1
        else:
            raise SyntaxError()
    
    def expression(self):
        if self.tokenList[self.pos].type == INTEGER:
            left_tree = numNode(self.tokenList[self.pos].value)
            self.eat(INTEGER)
            while self.tokenList[self.pos].type in OPERATORS:
                operator = self.tokenList[self.pos].type 
                self.eat(operator)
                right_tree = numNode(self.tokenList[self.pos].value)
                self.eat(INTEGER)
                left_tree = BinOpNode(operator,left_tree,right_tree)
        
        return left_tree
    
    def parse(self):
        root =  self.expression()
        self.eat(EOF)
        return root

class Interpreter():

    def __init__(self,root):
        self.ast = root
    
    def visit(self,node):

        if isinstance(node , numNode):
            return node.num
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
# TEST RUNNER
# ==================================================

def run_test(input_string):
    """Runs the full pipeline on a single input string."""
    print(f"Input: \"{input_string}\"")
    try:
        # 1. Lexer
        lexer = Lexer(input_string)
        lexer.tokenize()
        print(f"  Tokens: {lexer.list}")  # Optional: see the token list

        # 2. Parser
        parser = Parser(lexer.list)
        ast_root = parser.parse()
        print(f"  AST Root: {ast_root}")  # Optional: see the root node

        # 3. Interpreter
        interpreter = Interpreter(ast_root)
        result = interpreter.evaluate()
        
        print(f"  Result: {result}")
        
    except SyntaxError as e:
        print(f"  Syntax Error: {e} (Invalid syntax)")
    except Exception as e:
        print(f"  Unexpected Error: {e}")
    print("-" * 40)


# -------- RUN THE TESTS --------
print("========== INTERPRETER TEST SUITE ==========\n")

test_cases = [
    "3 + 4 - 2",          # Expected: 5
    "42",                 # Expected: 42
    "10 - 3 + 5",         # Expected: 12 (left-to-right)
    "100 + 20 - 30 + 10", # Expected: 100
    "3 +",                # Expected: Syntax Error (missing number)
    "3 + 4 5",            # Expected: Syntax Error (extra token)
]

for test in test_cases:
    run_test(test)

print("========== TESTS COMPLETE ==========")

