PLUS, EOF, MINUS, IDENTIFIER, ASSIGN, MUL, DIVIDE, DIV, MOD, KEYWORD = 'PLUS', 'EOF', 'MINUS', 'IDENTIFIER', 'ASSIGN', 'MULTIPLY', 'DIVIDE', 'DIV', 'MOD', 'KEYWORD'

# Removed DATATYPE dictionary and replaced with individual variables
INTEGER = 'INTEGER'
REAL = 'REAL'
STRING = 'STRING'

keyword_list = [
    'OUTPUT', 'INPUT', 'IF', 'THEN', 'ELSE', 'ENDIF', 
    'WHILE', 'DO', 'ENDWHILE', 'REPEAT', 'UNTIL', 
    'FOR', 'TO', 'NEXT', 'FUNCTION', 'PROCEDURE', 
    'RETURNS', 'ENDFUNCTION', 'ENDPROCEDURE', 'TRUE', 'FALSE'
]

KEYWORDS = {word: word for word in keyword_list}

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
            
            elif self.current_char == "*":
                self.advance()
                return Token(MUL, '*')
            
            elif self.current_char == "/":
                self.advance()
                return Token(DIVIDE, '/')
            
            elif self.current_char == "DIV":
                self.advance()
                return Token(DIV, 'DIV')
            
            elif self.current_char == "MOD":
                self.advance()
                return Token(MOD, 'MOD')
            
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

class OutputNode():
    def __init__(self,expression):
        self.expr = expression

class InputNode():
    def __init__(self,name):
        self.name = name
       


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
                 right_tree = self.expression()
            else:
                raise SyntaxError()
            
        return AssignNode(name, right_tree)

    def output_statement(self):
         if self.tokenList[self.pos].type == KEYWORD and self.tokenList[self.pos].value == KEYWORDS['OUTPUT'] :
             self.eat(KEYWORD)
             expression = self.expression()
             return OutputNode(expression)
         
    def input_statement(self):
         if self.tokenList[self.pos].type == KEYWORD and self.tokenList[self.pos].value == KEYWORDS['INPUT'] :
             self.eat(KEYWORD)
             if self.tokenList[self.pos].type == IDENTIFIER  :
                 name = self.tokenList[self.pos].value
                 self.eat(IDENTIFIER)
                 return InputNode(name)

    def parse(self):
        if self.tokenList[self.pos].type == EOF:
            return None
        
        if (self.pos + 1 < len(self.tokenList) and self.tokenList[self.pos].type == IDENTIFIER and self.tokenList[self.pos + 1].type == ASSIGN):
            node = self.assignment()

        elif  (self.tokenList[self.pos].type == KEYWORD and self.tokenList[self.pos].value == KEYWORDS['OUTPUT']):
            node = self.output_statement()

        elif  (self.tokenList[self.pos].type == KEYWORD and self.tokenList[self.pos].value == KEYWORDS['INPUT']):
            node = self.input_statement()

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

        elif isinstance(node, OutputNode):
            value = self.visit(node.expr)
            print(value)
            return None
        
        elif isinstance(node, InputNode):
            value = int(input())
            self.variables[node.name] = value
            return None
        
        else:
            left = self.visit(node.left)
            right = self.visit(node.right)

            if node.opr == PLUS:
                output = left + right

            elif node.opr == MINUS:
                output = left - right

            elif node.opr == MUL:
                output = left * right

            elif node.opr == DIVIDE:
                output = left / right
            
            elif node.opr == DIV:
                output = left - right
            
        return output
            
    def evaluate(self):
        return self.visit(self.ast)
    
# ==================================================
# COMPREHENSIVE TEST SUITE FOR ALL FEATURES (FIXED)
# ==================================================

print("\n" + "="*60)
print("   COMPREHENSIVE INTERPRETER TEST SUITE")
print("="*60 + "\n")

# --- SECTION 1: Isolated Unit Tests (Fresh Interpreter Each Time) ---
print("--- SECTION 1: Isolated Statements (Fresh Interpreter per test) ---\n")

isolated_tests = [
    # 1. Basic Expressions
    ("3 + 4", 7),
    ("42", 42),
    ("10 + 20 - 5", 25),
    ("100 - 30 + 10", 80),
    
    # 2. Variable Assignments
    ("x <-- 10", None),          # Stores x=10
    ("x <-- 3 + 4", None),       # Stores x=7
    
    # 3. OUTPUT Statement
    ("OUTPUT 42", None),         # Should print 42
    ("OUTPUT 3 + 4", None),      # Should print 7
    
    # 4. Error Handling
    ("3 +", None),               # Syntax Error (missing number)
    ("x + 2", None),             # Runtime Error (undefined variable)
]

def run_unit_test(input_string, expected):
    """Runs a single statement with a fresh interpreter."""
    print(f"Test: '{input_string}'")
    try:
        lexer = Lexer(input_string)
        lexer.tokenize()
        parser = Parser(lexer.list)
        ast = parser.parse()
        
        if ast is None:
            print("  Result: (Empty input)")
            return
        
        interpreter = Interpreter(ast)
        result = interpreter.evaluate()
        print(f"  Result: {result}")
        print(f"  Variables: {interpreter.variables}")
        
        # Check if result matches expected
        if expected is not None and result != expected:
            print(f"  ⚠️ Expected: {expected}")
        else:
            print("  ✅ Test Passed")
            
    except SyntaxError as e:
        print(f"  ❌ Syntax Error: {e}")
    except KeyError as e:
        print(f"  ❌ Runtime Error: Undefined variable {e}")
    except Exception as e:
        print(f"  ❌ Unexpected Error: {e}")
    print("-" * 40)

for test, expected in isolated_tests:
    run_unit_test(test, expected)


# --- SECTION 2: Sequential Statements (Same Interpreter) ---
print("\n--- SECTION 2: Sequential Statements (Same Interpreter) ---\n")

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
            
            # CRITICAL FIX: Create interpreter on first line, but ALWAYS execute
            if interpreter is None:
                interpreter = Interpreter(ast)
            
            # ALWAYS execute the current AST (whether first or subsequent)
            interpreter.visit(ast)
            
            # After execution, show the variable store
            print(f"  Variables: {interpreter.variables}")
            
        except SyntaxError as e:
            print(f"  ❌ Syntax Error: {e}")
            break
        except KeyError as e:
            print(f"  ❌ Runtime Error: Undefined variable {e}")
            break
        except Exception as e:
            print(f"  ❌ Unexpected Error: {e}")
            break
        print("-" * 30)


# Test Case A: Basic Sequential Program
print("--- Test A: Variables and OUTPUT ---")
program_a = [
    "x <-- 10",
    "OUTPUT x",          # Should print 10
    "y <-- x + 2",       # y = 12
    "OUTPUT y",          # Should print 12
    "OUTPUT x + y",      # Should print 22
]
run_sequential_program(program_a)


# Test Case B: Sequential Program with INPUT
print("\n--- Test B: Variables, INPUT, and OUTPUT ---")
print("‼️ IMPORTANT: When prompted for INPUT, type a number (e.g., 5) and press Enter.")
program_b = [
    "x <-- 3",
    "OUTPUT x",          # Prints 3
    "INPUT y",           # Waits for user input (type 5)
    "OUTPUT y",          # Prints user input (5)
    "OUTPUT x + y",      # Prints 8 (3 + 5)
]
run_sequential_program(program_b)


# Test Case C: Complex Calculations
print("\n--- Test C: Complex Calculations ---")
program_c = [
    "a <-- 10 + 5",      # a = 15
    "b <-- a - 3",       # b = 12
    "c <-- b * 2",       # c = 24
    "OUTPUT c",          # Should print 24
    "OUTPUT a + b + c",  # Should print 51 (15 + 12 + 24)
]
run_sequential_program(program_c)


print("\n" + "="*60)
print("   ALL TESTS COMPLETE")
print("="*60)# ==================================================
# COMPREHENSIVE TEST SUITE FOR ALL FEATURES (FIXED)
# ==================================================

print("\n" + "="*60)
print("   COMPREHENSIVE INTERPRETER TEST SUITE")
print("="*60 + "\n")

# --- SECTION 1: Isolated Unit Tests (Fresh Interpreter Each Time) ---
print("--- SECTION 1: Isolated Statements (Fresh Interpreter per test) ---\n")

isolated_tests = [
    # 1. Basic Expressions
    ("3 + 4", 7),
    ("42", 42),
    ("10 + 20 - 5", 25),
    ("100 - 30 + 10", 80),
    
    # 2. Variable Assignments
    ("x <-- 10", None),          # Stores x=10
    ("x <-- 3 + 4", None),       # Stores x=7
    
    # 3. OUTPUT Statement
    ("OUTPUT 42", None),         # Should print 42
    ("OUTPUT 3 + 4", None),      # Should print 7
    
    # 4. Error Handling
    ("3 +", None),               # Syntax Error (missing number)
    ("x + 2", None),             # Runtime Error (undefined variable)
]

def run_unit_test(input_string, expected):
    """Runs a single statement with a fresh interpreter."""
    print(f"Test: '{input_string}'")
    try:
        lexer = Lexer(input_string)
        lexer.tokenize()
        parser = Parser(lexer.list)
        ast = parser.parse()
        
        if ast is None:
            print("  Result: (Empty input)")
            return
        
        interpreter = Interpreter(ast)
        result = interpreter.evaluate()
        print(f"  Result: {result}")
        print(f"  Variables: {interpreter.variables}")
        
        # Check if result matches expected
        if expected is not None and result != expected:
            print(f"  ⚠️ Expected: {expected}")
        else:
            print("  ✅ Test Passed")
            
    except SyntaxError as e:
        print(f"  ❌ Syntax Error: {e}")
    except KeyError as e:
        print(f"  ❌ Runtime Error: Undefined variable {e}")
    except Exception as e:
        print(f"  ❌ Unexpected Error: {e}")
    print("-" * 40)

for test, expected in isolated_tests:
    run_unit_test(test, expected)


# --- SECTION 2: Sequential Statements (Same Interpreter) ---
print("\n--- SECTION 2: Sequential Statements (Same Interpreter) ---\n")

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
            
            # CRITICAL FIX: Create interpreter on first line, but ALWAYS execute
            if interpreter is None:
                interpreter = Interpreter(ast)
            
            # ALWAYS execute the current AST (whether first or subsequent)
            interpreter.visit(ast)
            
            # After execution, show the variable store
            print(f"  Variables: {interpreter.variables}")
            
        except SyntaxError as e:
            print(f"  ❌ Syntax Error: {e}")
            break
        except KeyError as e:
            print(f"  ❌ Runtime Error: Undefined variable {e}")
            break
        except Exception as e:
            print(f"  ❌ Unexpected Error: {e}")
            break
        print("-" * 30)


# Test Case A: Basic Sequential Program
print("--- Test A: Variables and OUTPUT ---")
program_a = [
    "x <-- 10",
    "OUTPUT x",          # Should print 10
    "y <-- x + 2",       # y = 12
    "OUTPUT y",          # Should print 12
    "OUTPUT x + y",      # Should print 22
]
run_sequential_program(program_a)


# Test Case B: Sequential Program with INPUT
print("\n--- Test B: Variables, INPUT, and OUTPUT ---")
print("‼️ IMPORTANT: When prompted for INPUT, type a number (e.g., 5) and press Enter.")
program_b = [
    "x <-- 3",
    "OUTPUT x",          # Prints 3
    "INPUT y",           # Waits for user input (type 5)
    "OUTPUT y",          # Prints user input (5)
    "OUTPUT x + y",      # Prints 8 (3 + 5)
]
run_sequential_program(program_b)


# Test Case C: Complex Calculations
print("\n--- Test C: Complex Calculations ---")
program_c = [
    "a <-- 10 + 5",      # a = 15
    "b <-- a - 3",       # b = 12
    "c <-- b * 2",       # c = 24
    "OUTPUT c",          # Should print 24
    "OUTPUT a + b + c",  # Should print 51 (15 + 12 + 24)
]
run_sequential_program(program_c)


print("\n" + "="*60)
print("   ALL TESTS COMPLETE")
print("="*60)