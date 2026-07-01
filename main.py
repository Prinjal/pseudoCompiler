INTEGER , PLUS , EOF , MINUS = 'INTEGER','PLUS','EOF' , 'MINUS'

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
    
lexer = Lexer("3 + 4 - 2")
while True:
    tok = lexer.get_next_token()
    print(tok)
    if tok.type == EOF:
        break
