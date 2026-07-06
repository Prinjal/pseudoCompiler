PLUS, EOF, MINUS, IDENTIFIER, ASSIGN, MUL, DIVIDE, DIV, MOD,LPAREN,RPAREN, KEYWORD,COLON , EQ, NE, LT, GT, LE, GE = 'PLUS', 'EOF', 'MINUS', 'IDENTIFIER', 'ASSIGN', 'MULTIPLY', 'DIVIDE', 'DIV', 'MOD','(',')', 'KEYWORD',':','EQ','NE','LT','GT','LE','GE'

INTEGER = 'INTEGER'
REAL = 'REAL'
STRING = 'STRING'
BOOLEAN = 'BOOLEAN'

keyword_list = [
    'OUTPUT', 'INPUT', 'IF', 'THEN', 'ELSE', 'ENDIF', 
    'WHILE', 'DO', 'ENDWHILE', 'REPEAT', 'UNTIL', 
    'FOR', 'TO', 'NEXT', 'FUNCTION', 'PROCEDURE', 
    'RETURNS', 'ENDFUNCTION', 'ENDPROCEDURE', 'TRUE', 'FALSE','DIV', 'MOD','DECLARE'
]

TYPE_MAP = {
    int: 'INTEGER',
    float: 'REAL',
    str: 'STRING',
    bool: 'BOOLEAN'
}

KEYWORDS = {word: word for word in keyword_list}

OPERATORS = [MINUS, PLUS, MUL, DIVIDE, MOD, DIV , EQ, NE, LT, GT, LE, GE]


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
    
    def string(self):
        result = ""
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()
        if self.current_char == None:
            SyntaxError("Unclosed string literal")

        self.advance()
        return result
    
    def word(self):
        result = ""
        while self.current_char and  (self.current_char.isalnum() or self.current_char == '_'):
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

    def decimal(self):
        result = ""
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            elif self.current_char.isdigit():    
                number = self.integer()
                if self.current_char == ".":
                   self.advance()
                   deciDigits = self.decimal()
                   if len(deciDigits) < 1 :
                        raise TypeError("Invalid Format")
                   return Token(REAL,float(f"{number}.{deciDigits}"))

                return Token(INTEGER, number)
            
            elif self.current_char == '"':
                self.advance()
                word = self.string()
                return Token(STRING,word)
               
            elif self.current_char == '>':
              if self.pos + 1 < len(self.text):
                if self.text[self.pos+1] == '=':
                    self.advance()
                    self.advance()
                    return Token(GE,">=")
                else:
                    self.advance()
                    return Token(GT,">")
               


            elif self.current_char.isalpha():
                word = self.word()

                if word == "TRUE":
                    return Token(BOOLEAN, True)
                
                elif word == "FALSE":
                    return Token(BOOLEAN, False)

                elif word in ("INTEGER", "REAL", "STRING", "BOOLEAN"):
                    return Token(word, word)

                elif word in KEYWORDS:
                    if word == "DIV":
                        return Token(DIV, 'DIV')
                    elif word == "MOD":
                        return Token(MOD, 'MOD')
                    
                    return Token(KEYWORD, word)

                return Token(IDENTIFIER, word)
                
            
            elif self.current_char == "+":
                self.advance()
                return Token(PLUS, '+')
            
            elif self.current_char == '=':
                self.advance()
                return Token(EQ, '=')
            
            elif self.current_char == "<":
                if self.pos + 1 < len(self.text):
                    nextChar1 = self.text[self.pos+1]

                    if nextChar1 == "-":
                        nextChar2 = self.text[self.pos+2]
                        if nextChar2 == "-":
                            self.advance()
                            self.advance()
                            self.advance()
                            return Token(ASSIGN, '<--')
                    
                    if nextChar1 == '=':
                        self.advance()
                        self.advance()
                        return Token(LE,"<=")
                        
                    elif nextChar1 == ">":
                        self.advance()
                        self.advance()
                        return Token(NE,"<>")
                    else:
                        self.advance()
                        return Token(LT,"<")
               
            
            elif self.current_char == "-":
                self.advance()
                return Token(MINUS, '-')
            
            elif self.current_char == ":":
                self.advance()
                return Token(COLON, ':')
            
            elif self.current_char == "*":
                self.advance()
                return Token(MUL, '*')
            
            elif self.current_char == "/":
                self.advance()
                return Token(DIVIDE, '/')
            
            elif self.current_char == "(":
                self.advance()
                return Token(LPAREN, '(')

            elif self.current_char == ")":
                self.advance()
                return Token(RPAREN, ')')
            
            else:
                self.error()

        return Token(EOF, None)
    
class varNode():
    def __init__(self, name):
        self.name = name

class intNode():
    def __init__(self, num):
        self.num = num

class realNode():
    def __init__(self, num):
        self.num = num

class boolNode():
    def __init__(self, value):
        self.value = value

class strNode():
    def __init__(self, text):
        self.text = text

class BinOpNode():
    def __init__(self, operation, left, right):
        self.opr = operation
        self.left = left
        self.right = right

class CompareNode():
    def __init__(self, operation, left, right):
        self.opr = operation
        self.left = left
        self.right = right

class AssignNode():
    def __init__(self, name, expression):
        self.name = name
        self.expr = expression

class OutputNode():
    def __init__(self,expression):
        self.expr = expression

class InputNode():
    def __init__(self,name):
        self.name = name

class DeclareNode():
    def __init__(self,name,Dtype):
        self.name = name
        self.Dtype = Dtype


class Parser():
    def __init__(self, list):
        self.tokenList = list
        self.pos = 0

    def eat(self, expected_type):
        if self.tokenList[self.pos].type == expected_type:
            self.pos += 1
        else:
            raise SyntaxError()
    
    def term(self):
        leftNode = self.factor()
        while self.tokenList[self.pos].type in [MUL,DIVIDE,DIV,MOD]:
            operator = self.tokenList[self.pos].type
            self.eat(operator)
            rightNode = self.factor()
            leftNode = BinOpNode(operator, leftNode, rightNode)
        
        return leftNode

    def factor(self):
        if self.tokenList[self.pos].type == IDENTIFIER:
            node = varNode(self.tokenList[self.pos].value)
            self.eat(IDENTIFIER)
            return node

        elif self.tokenList[self.pos].type == INTEGER:  
            node = intNode(self.tokenList[self.pos].value)
            self.eat(INTEGER)     
            return node  
        
        elif self.tokenList[self.pos].type == REAL:  
            node = realNode(self.tokenList[self.pos].value)
            self.eat(REAL)     
            return node  
        
        elif self.tokenList[self.pos].type == STRING:
            node = strNode(self.tokenList[self.pos].value)
            self.eat(STRING)
            return node

        elif self.tokenList[self.pos].type == BOOLEAN:
            node = boolNode(self.tokenList[self.pos].value)
            self.eat(BOOLEAN)
            return node

        elif self.tokenList[self.pos].type == LPAREN:  
            self.eat(LPAREN)    
            node = self.comparision() 
            self.eat(RPAREN)
            return node     
        
        else:
                raise SyntaxError()
    def comparision(self):
        left = self.expression()
        while self.tokenList[self.pos].type in [EQ,NE,GT,LT,GE,LE]:
            operator = self.tokenList[self.pos].type
            self.eat(operator)
            right = self.expression()
            left = CompareNode(operator,left,right)
        
        return left

    def expression(self):
        left_tree = self.term()
        while self.tokenList[self.pos].type in [PLUS , MINUS]:
            operator = self.tokenList[self.pos].type 
            self.eat(operator)
            right_tree = self.term()
            left_tree = BinOpNode(operator, left_tree, right_tree)
        
        return left_tree
    
    def assignment(self):
        if self.tokenList[self.pos].type == IDENTIFIER:
            name = self.tokenList[self.pos].value
            self.eat(IDENTIFIER)
            if self.tokenList[self.pos].type == ASSIGN:
                 self.eat(ASSIGN)
                 right_tree = self.comparision()
            else:
                raise SyntaxError()
            
        return AssignNode(name, right_tree)

    def output_statement(self):
         if self.tokenList[self.pos].type == KEYWORD and self.tokenList[self.pos].value == KEYWORDS['OUTPUT'] :
             self.eat(KEYWORD)
             expression = self.comparision()
             return OutputNode(expression)
         
    def input_statement(self):
         if self.tokenList[self.pos].type == KEYWORD and self.tokenList[self.pos].value == KEYWORDS['INPUT'] :
             self.eat(KEYWORD)
             if self.tokenList[self.pos].type == IDENTIFIER  :
                 name = self.tokenList[self.pos].value
                 self.eat(IDENTIFIER)
                 return InputNode(name)

    def declare_statement(self):
         if self.tokenList[self.pos].type == KEYWORD and self.tokenList[self.pos].value == KEYWORDS['DECLARE'] :
             self.eat(KEYWORD)
             if self.tokenList[self.pos].type == IDENTIFIER :
                name = self.tokenList[self.pos].value
                self.eat(IDENTIFIER)
                if self.tokenList[self.pos].type == COLON :
                    self.eat(COLON)
                    if self.tokenList[self.pos].type in [INTEGER, REAL, STRING, BOOLEAN] :
                        Dtype = self.tokenList[self.pos].type
                        self.eat(Dtype)
                        return DeclareNode(name,Dtype)


             
    def parse(self):
        if self.tokenList[self.pos].type == EOF:
            return None
        
        elif  (self.tokenList[self.pos].type == KEYWORD and self.tokenList[self.pos].value == KEYWORDS['DECLARE']):
            node = self.declare_statement()


        elif  (self.tokenList[self.pos].type == KEYWORD and self.tokenList[self.pos].value == KEYWORDS['OUTPUT']):
            node = self.output_statement()

        elif  (self.tokenList[self.pos].type == KEYWORD and self.tokenList[self.pos].value == KEYWORDS['INPUT']):
            node = self.input_statement()

        elif (self.pos + 1 < len(self.tokenList) and self.tokenList[self.pos].type == IDENTIFIER and self.tokenList[self.pos + 1].type == ASSIGN):
            node = self.assignment()

        else:
            node = self.comparision()


        self.eat(EOF)
        return node
     
       
        


class Interpreter():

    def __init__(self, root):
        self.ast = root
        self.symbols = {}
       
    def visit(self, node):

        if isinstance(node, DeclareNode):
            if node.Dtype == INTEGER:
                self.symbols[node.name] = {'Value':0,'Type':node.Dtype}

            elif node.Dtype == REAL:
                self.symbols[node.name] = {'Value':0.00,'Type':node.Dtype}
            
            elif node.Dtype == STRING:
                self.symbols[node.name] = {'Value':'','Type':node.Dtype}

            elif node.Dtype == BOOLEAN:
                self.symbols[node.name] = {'Value':False,'Type':node.Dtype}

            return None
        
        elif isinstance(node, intNode):
            return node.num
        
        elif isinstance(node, realNode):
            return node.num
        
        elif isinstance(node, strNode):
            return node.text
        
        elif isinstance(node, boolNode):
            return node.value
        
        elif isinstance(node, varNode):
            if node.name in self.symbols:
                return self.symbols[node.name]['Value']
            else:
                raise RuntimeError("Variable not declared")
        

        elif isinstance(node, AssignNode):
            if node.name in self.symbols:
                value = self.visit(node.expr)
                if TYPE_MAP.get(type(value),"Unknown") == self.symbols[node.name]['Type']:
                    self.symbols[node.name]['Value'] =  value
                    return value
                else:
                   raise TypeError()
            else:
                   raise RuntimeError(f"Variable '{node.name}' not declared")

        elif isinstance(node, OutputNode):
            value = self.visit(node.expr)
            print(value)
            return None
        
        elif isinstance(node,CompareNode):
            left_val = self.visit(node.left)
            right_val = self.visit(node.right)
            
            if node.opr == EQ:   return left_val == right_val
            if node.opr == NE:   return left_val != right_val
            if node.opr == LT:   return left_val < right_val
            if node.opr == GT:   return left_val > right_val
            if node.opr == LE:   return left_val <= right_val
            if node.opr == GE:   return left_val >= right_val

        elif isinstance(node, InputNode):
            if node.name in self.symbols:
                value = input()
                if len(value) < 1:
                    raise RuntimeError("Input must not be empty")
                
                if self.symbols[node.name]["Type"] == INTEGER:
                    try:
                        self.symbols[node.name]["Value"] = int(value)
                    except ValueError:
                        raise TypeError(f"Input '{value}' cannot be converted to {self.symbols[node.name]["Type"]}")


                elif self.symbols[node.name]["Type"] == REAL:

                    try:
                        self.symbols[node.name]['Value'] = float(value)
                    except ValueError:
                        raise TypeError(f"Input '{value}' cannot be converted to {self.symbols[node.name]["Type"]}")
                
                elif self.symbols[node.name]["Type"] == STRING:
                    
                        self.symbols[node.name]['Value'] = str(value)

                elif self.symbols[node.name]["Type"] == BOOLEAN:
                    if value.upper() == "TRUE":
                        self.symbols[node.name]['Value'] = True
                    elif value.upper() == "FALSE":
                        self.symbols[node.name]['Value'] = False
                    else:
                        raise TypeError(f"Input '{value}' cannot be converted to BOOLEAN")
                    
                else:
                    raise TypeError()
                
            else:
                   raise RuntimeError(f"Variable '{node.name}' not declared")
            
            return None
        
        else:
            left = self.visit(node.left)
            right = self.visit(node.right)
            if type(left) != type(right):
                raise RuntimeError("Invalid operations")
            
            if node.opr == PLUS:
                output = left + right

            elif node.opr == MINUS:
                output = left - right

            elif node.opr == MUL:
                output = left * right

            elif node.opr == DIVIDE:
                output = left / right
            
            elif node.opr == DIV:
                output = left // right
            
            elif node.opr == MOD:
                output = left % right
            
            return output
            
    def evaluate(self):
        return self.visit(self.ast)
    
# ==================================================
# COMPLETE TEST SUITE - INCLUDING COMPARISONS
# ==================================================

print("\n" + "="*70)
print("   COMPLETE INTERPRETER TEST SUITE (WITH COMPARISONS)")
print("="*70 + "\n")

# --- SECTION 1: Isolated Unit Tests ---
print("--- SECTION 1: Isolated Statements (Fresh Interpreter Each Time) ---\n")

isolated_tests = [
    # ----- BASIC EXPRESSIONS -----
    ("3 + 4", 7),
    ("42", 42),
    ("10 + 20 - 5", 25),
    ("100 - 30 + 10", 80),
    ("2 * 3 + 4", 10),
    ("2 + 3 * 4", 14),
    ("(2 + 3) * 4", 20),
    ("10 / 2", 5.0),
    ("10 DIV 3", 3),
    ("10 MOD 3", 1),
    
    # ----- INTEGER COMPARISONS -----
    ("3 = 3", True),
    ("3 = 4", False),
    ("3 <> 4", True),
    ("3 <> 3", False),
    ("3 < 4", True),
    ("3 < 3", False),
    ("3 > 4", False),
    ("3 > 3", False),
    ("3 <= 4", True),
    ("3 <= 3", True),
    ("3 <= 2", False),
    ("3 >= 4", False),
    ("3 >= 3", True),
    ("3 >= 2", True),
    
    # ----- COMPARISONS WITH EXPRESSIONS -----
    ("3 + 4 = 7", True),
    ("3 + 4 = 8", False),
    ("10 - 3 > 5", True),
    ("10 - 3 > 7", False),
    ("2 * 3 + 4 = 10", True),
    ("2 + 3 * 4 = 14", True),
    ("(2 + 3) * 4 = 20", True),
    ("10 / 2 = 5", True),
    
    # ----- REAL COMPARISONS -----
    ("3.14 = 3.14", True),
    ("3.14 = 3.15", False),
    ("3.14 <> 3.15", True),
    ("3.14 < 3.15", True),
    ("3.14 > 3.15", False),
    ("3.14 <= 3.14", True),
    ("3.14 >= 3.14", True),
    
    # ----- MIXED TYPE COMPARISONS (Integer vs Real) -----
    ("3 = 3.0", True),
    ("3 = 3.1", False),
    ("3 < 3.1", True),
    ("3 > 3.1", False),
    ("3 <= 3.0", True),
    ("3 >= 3.0", True),
    ("4 > 3.5", True),
    ("4 < 3.5", False),
    
    # ----- STRING COMPARISONS -----
    ('"Hello" = "Hello"', True),
    ('"Hello" = "World"', False),
    ('"Hello" <> "World"', True),
    ('"A" < "B"', True),
    ('"B" < "A"', False),
    ('"A" <= "A"', True),
    ('"A" >= "A"', True),
    
    # ----- BOOLEAN COMPARISONS -----
    ("TRUE = TRUE", True),
    ("TRUE = FALSE", False),
    ("TRUE <> FALSE", True),
    
    # ----- VARIABLE DECLARATIONS -----
    ("DECLARE x : INTEGER", None),
    ("DECLARE y : REAL", None),
    ('DECLARE name : STRING', None),
    ("DECLARE flag : BOOLEAN", None),
    
    # ----- VARIABLE ASSIGNMENTS -----
    ("x <-- 10", None),
    ("y <-- 3.14", None),
    ('name <-- "Hello"', None),
    ("flag <-- TRUE", None),
    
    # ----- VARIABLE COMPARISONS -----
    ("x = 10", True),
    ("x = 11", False),
    ("x > 5", True),
    ("x < 5", False),
    ("y = 3.14", True),
    ("y <> 3.15", True),
    ('name = "Hello"', True),
    ('name = "World"', False),
    ("flag = TRUE", True),
    ("flag = FALSE", False),
    
    # ----- COMPARISONS WITH VARIABLES AND EXPRESSIONS -----
    ("x + 5 = 15", True),
    ("x * 2 = 20", True),
    ("x / 2 = 5", True),
    ("x DIV 3 = 3", True),
    ("x MOD 3 = 1", True),
    ("x > 5 AND x < 20", None),  # Will test once AND is implemented
    
    # ----- OUTPUT STATEMENTS -----
    ("OUTPUT 42", None),
    ("OUTPUT 3 + 4", None),
    ('OUTPUT "Hello"', None),
    ("OUTPUT TRUE", None),
    ("OUTPUT x = 10", None),      # Should print True
    ("OUTPUT x > 5", None),       # Should print True
    ("OUTPUT y = 3.14", None),    # Should print True
    
    # ----- ERROR HANDLING -----
    ("3 +", None),                # Syntax Error
    ("x + 2", None),              # Runtime Error (x not declared)
    ("3 =", None),                # Syntax Error (missing right side)
    ("= 3", None),                # Syntax Error (missing left side)
]

def run_unit_test(input_string, expected):
    """Runs a single statement with a fresh interpreter."""
    print(f"Test: '{input_string}'")
    try:
        lexer = Lexer(input_string)
        lexer.tokenize()
        # Uncomment to see tokens:
        # print(f"  Tokens: {lexer.list}")
        
        parser = Parser(lexer.list)
        ast = parser.parse()
        
        if ast is None:
            print("  Result: (Empty input)")
            return
        
        interpreter = Interpreter(ast)
        result = interpreter.evaluate()
        print(f"  Result: {result}")
        print(f"  Variables: {interpreter.symbols}")
        
        if expected is not None and result != expected:
            print(f"  ⚠️ Expected: {expected}")
        else:
            print("  ✅ Test Passed")
            
    except SyntaxError as e:
        print(f"  ❌ Syntax Error: {e}")
    except KeyError as e:
        print(f"  ❌ Runtime Error: Undefined variable {e}")
    except TypeError as e:
        print(f"  ❌ Type Error: {e}")
    except RuntimeError as e:
        print(f"  ❌ Runtime Error: {e}")
    except Exception as e:
        print(f"  ❌ Unexpected Error: {e}")
    print("-" * 40)

for test, expected in isolated_tests:
    run_unit_test(test, expected)


# --- SECTION 2: Sequential Programs (Same Interpreter) ---
print("\n--- SECTION 2: Sequential Programs (Same Interpreter) ---\n")

def run_sequential_program(program_lines):
    """Runs multiple statements using the SAME interpreter."""
    interpreter = None
    
    for i, line in enumerate(program_lines):
        print(f"Line {i+1}: '{line}'")
        try:
            lexer = Lexer(line)
            lexer.tokenize()
            parser = Parser(lexer.list)
            ast = parser.parse()
            
            if ast is None:
                print("  Skipping empty line.")
                continue
            
            if interpreter is None:
                interpreter = Interpreter(ast)
            else:
                interpreter.visit(ast)
            
            print(f"  Variables: {interpreter.symbols}")
            
        except SyntaxError as e:
            print(f"  ❌ Syntax Error: {e}")
            break
        except KeyError as e:
            print(f"  ❌ Runtime Error: Undefined variable {e}")
            break
        except TypeError as e:
            print(f"  ❌ Type Error: {e}")
            break
        except RuntimeError as e:
            print(f"  ❌ Runtime Error: {e}")
            break
        except Exception as e:
            print(f"  ❌ Unexpected Error: {e}")
            break
        print("-" * 30)


# --- Test A: INTEGER Variables with Comparisons ---
print("\n--- Test A: INTEGER Variables with Comparisons ---")
program_a = [
    "DECLARE x : INTEGER",
    "DECLARE result1 : BOOLEAN",
    "DECLARE result2 : BOOLEAN",
    "DECLARE result3 : BOOLEAN",
    "x <-- 10",
    "result1 <-- x = 10",
    "result2 <-- x > 5",
    "result3 <-- x < 5",
    "OUTPUT result1",
    "OUTPUT result2",
    "OUTPUT result3",
]
run_sequential_program(program_a)


# --- Test B: REAL Variables with Comparisons ---
print("\n--- Test B: REAL Variables with Comparisons ---")
program_b = [
    "DECLARE x : REAL",
    "DECLARE y : REAL",
    "DECLARE result1 : BOOLEAN",
    "DECLARE result2 : BOOLEAN",
    "x <-- 3.14",
    "y <-- 2.71",
    "result1 <-- x > y",
    "result2 <-- x <= y",
    "OUTPUT result1",
    "OUTPUT result2",
]
run_sequential_program(program_b)


# --- Test C: STRING Variables with Comparisons ---
print("\n--- Test C: STRING Variables with Comparisons ---")
program_c = [
    'DECLARE name1 : STRING',
    'DECLARE name2 : STRING',
    'DECLARE result1 : BOOLEAN',
    'DECLARE result2 : BOOLEAN',
    'name1 <-- "Hello"',
    'name2 <-- "World"',
    'result1 <-- name1 = "Hello"',
    'result2 <-- name1 <> name2',
    'OUTPUT result1',
    'OUTPUT result2',
]
run_sequential_program(program_c)


# --- Test D: Complex Comparisons with Expressions ---
print("\n--- Test D: Complex Comparisons with Expressions ---")
program_d = [
    "DECLARE x : INTEGER",
    "DECLARE y : REAL",
    "DECLARE result1 : BOOLEAN",
    "DECLARE result2 : BOOLEAN",
    "x <-- 10",
    "y <-- 3.14",
    "result1 <-- x + 5 = 15",
    "result2 <-- x / 2 = y",     # 10/2 = 5, y = 3.14 → False
    "OUTPUT result1",
    "OUTPUT result2",
]
run_sequential_program(program_d)


# --- Test E: OUTPUT with Comparisons ---
print("\n--- Test E: OUTPUT with Comparisons ---")
program_e = [
    "DECLARE x : INTEGER",
    "x <-- 10",
    "OUTPUT x = 10",    # Should print True
    "OUTPUT x > 5",     # Should print True
    "OUTPUT x < 5",     # Should print False
    "OUTPUT x <> 10",   # Should print False
]
run_sequential_program(program_e)


# --- SECTION 3: Lexer-Only Tests (Data Type Recognition) ---
print("\n--- SECTION 3: Lexer-Only Tests (Data Type Recognition) ---\n")

def test_lexer(input_string):
    """Runs only the lexer to show token stream."""
    print(f"Input: '{input_string}'")
    try:
        lexer = Lexer(input_string)
        lexer.tokenize()
        print(f"  Tokens: {lexer.list}")
        print("  ✅ Lexer passed")
    except Exception as e:
        print(f"  ❌ Lexer Error: {e}")
    print("-" * 40)

print("Testing Data Type Recognition in Lexer:")
test_lexer("42")
test_lexer("3.14")
test_lexer('"Hello"')
test_lexer("TRUE")
test_lexer("FALSE")
test_lexer("DECLARE x : INTEGER")
test_lexer('DECLARE name : STRING')
test_lexer("3 + 4.2")
test_lexer('OUTPUT "Hello" + " World"')
test_lexer("x <-- TRUE")
test_lexer("3 = 3")
test_lexer("3 <> 4")
test_lexer("3 <= 4")
test_lexer("3 >= 4")
test_lexer("x < 5")
test_lexer("x > 5")


# --- SECTION 4: Comparison-Only Tests ---
print("\n--- SECTION 4: Comparison-Only Tests ---\n")

comparison_tests = [
    ("3 = 3", True),
    ("3 = 4", False),
    ("3 <> 4", True),
    ("3 <> 3", False),
    ("3 < 4", True),
    ("3 < 3", False),
    ("3 > 4", False),
    ("3 > 3", False),
    ("3 <= 4", True),
    ("3 <= 3", True),
    ("3 <= 2", False),
    ("3 >= 4", False),
    ("3 >= 3", True),
    ("3 >= 2", True),
    ("3 + 4 = 7", True),
    ("3 + 4 = 8", False),
    ("10 - 3 > 5", True),
    ("10 - 3 > 7", False),
    ("2 * 3 + 4 = 10", True),
    ("2 + 3 * 4 = 14", True),
    ("(2 + 3) * 4 = 20", True),
]

print("Running Comparison-Only Tests:")
for input_str, expected in comparison_tests:
    print(f"Test: '{input_str}'")
    try:
        lexer = Lexer(input_str)
        lexer.tokenize()
        parser = Parser(lexer.list)
        ast = parser.parse()
        interpreter = Interpreter(ast)
        result = interpreter.evaluate()
        if result == expected:
            print(f"  Result: {result} ✅")
        else:
            print(f"  Result: {result} ❌ Expected: {expected}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    print("-" * 20)

print("\n" + "="*70)
print("   ALL TESTS COMPLETE")
print("="*70)