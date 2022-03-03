import sys
from os import error



########################################################################

class Token():
    def __init__(self, type,value):
        self.type = type
        self.value = value
class Tokenizer():
    def __init__(self):
        self.origin = sys.argv[1]
        self.position = 0
        self.actual = Token("Init", "")
    def selectNext(self):

        if self.position >= len(self.origin):
            
            self.actual = Token("EOF","")
            return self.actual

        while self.origin[self.position] == " " and self.position < len(self.origin):
            self.position += 1
        if self.origin[self.position] == "+":
            self.position+=1
            self.actual = Token("PLUS","")
            return self.actual
        elif self.origin[self.position] == "-":
            self.position+=1
            self.actual = Token("MINUS","")
            return self.actual
        elif self.origin[self.position].isnumeric():
            algarismos = self.origin[self.position]
            self.position += 1
            while self.origin[self.position].isnumeric():
                algarismos += self.origin[self.position]
                self.position += 1
                if self.position >= len(self.origin):
                    break
            self.actual = Token("NUMBER",int(algarismos))
            return self.actual
        else:
            raise error


        

class Parser():
    tokens = Tokenizer()
    result = 0
    def parseExpession():
        
        Parser.tokens.selectNext()
        if Parser.tokens.actual.type == "NUMBER":
            result = Parser.tokens.actual.value
            Parser.tokens.selectNext()
                
            while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS":
                if Parser.tokens.actual.type == "PLUS":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "NUMBER":
                        result += Parser.tokens.actual.value
                    else:
                        raise error
                if Parser.tokens.actual.type == "MINUS":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "NUMBER":
                        result -= Parser.tokens.actual.value
                    else:
                        raise error
            
                Parser.tokens.selectNext()
            return result
        else:
            return error

    def run():
        resultado = Parser.parseExpession()
        return resultado
if __name__ == '__main__':
    result = Parser.run()
    print(result)



        