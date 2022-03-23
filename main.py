import sys
from os import error
import re

from httplib2 import RETRIES

class Token():
    def __init__(self, type,value):
        self.type = type
        self.value = value
class Tokenizer():
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = Token("Init", "")

    def selectNext(self):

        if self.position >= len(self.origin):
            
            self.actual = Token("EOF","")
            return self.actual

        while self.origin[self.position] == " " and self.position < len(self.origin):
            self.position += 1
            if self.position >= len(self.origin):
                self.actual = Token("EOF","")
                return self.actual
        
        if self.origin[self.position] == "+":
            self.position+=1
            self.actual = Token("PLUS","")
            return self.actual
        elif self.origin[self.position] == "-":
            self.position+=1
            self.actual = Token("MINUS","")
            return self.actual
        elif self.origin[self.position] == "*":
            self.position+=1
            self.actual = Token("MULTIPLICATION","")
            return self.actual
        elif self.origin[self.position] == "/":
            self.position+=1
            self.actual = Token("DIVISION","")
            return self.actual
        elif self.origin[self.position] == "(":
            self.position+=1
            self.actual = Token("OPEN-P","")
            return self.actual
        elif self.origin[self.position] == ")":
            self.position+=1
            self.actual = Token("CLOSE-P","")
            return self.actual
        elif self.origin[self.position].isnumeric():
            algarismos = self.origin[self.position]
            self.position += 1
            if self.position >= len(self.origin):
                self.actual = Token("NUMBER",int(algarismos))
                return self.actual
            while self.origin[self.position] == " ":
                if self.position + 1 < len(self.origin):
                    self.position += 1
                    if self.origin[self.position].isnumeric():
                        raise error
                else:
                    break
            while self.origin[self.position].isnumeric():
                algarismos += self.origin[self.position]
                self.position += 1
                if self.position >= len(self.origin):
                    break
            self.actual = Token("NUMBER",int(algarismos))
            return self.actual 
        else:
            raise error
class PrePro():
    def filter(origin):
        origin2 = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,origin)
        return origin2

class Parser():
    @staticmethod
    def parseTerm(tokens):
        resultado = 0
        resultado = Parser.parseFactor(tokens)
        if tokens.actual.type != "MULTIPLICATION" and tokens.actual.type != "DIVISION":
            return resultado
            
        while tokens.actual.type == "MULTIPLICATION" or tokens.actual.type == "DIVISION":
            if tokens.actual.type == "MULTIPLICATION":
                resultado *= int(Parser.parseFactor(tokens))
            if tokens.actual.type == "DIVISION":
                resultado /= Parser.parseFactor(tokens)
                
        return resultado
        
    @staticmethod
    def parseExpression(tokens):

        resultado = Parser.parseTerm(tokens)
        #Parser.tokens.selectNext()
        if tokens.actual.type == "PLUS" or tokens.actual.type == "MINUS" or tokens.actual.type == "EOF" or tokens.actual.type == "CLOSE-P":
                
            while tokens.actual.type == "PLUS" or tokens.actual.type == "MINUS":
                if tokens.actual.type == "PLUS":
                
                    resultado += Parser.parseTerm(tokens)
                    
                elif tokens.actual.type == "MINUS":
                    
                    resultado -= Parser.parseTerm(tokens)

            
            if tokens.actual.type == "EOF" or tokens.actual.type == "CLOSE-P":  
                return int(resultado)
            else:
                raise error
        else:
            raise error

    @staticmethod
    def parseFactor(tokens):
        tokens.selectNext()
        if tokens.actual.type == "NUMBER":
            resultado = tokens.actual.value
            tokens.selectNext()
        elif tokens.actual.type == "PLUS":
            resultado += Parser.parseFactor(tokens)
        elif tokens.actual.type == "MINUS":
            resultado -= Parser.parseFactor(tokens)
        elif tokens.actual.type == "OPEN-P":
            
            resultado = Parser.parseExpression(tokens)
            if tokens.actual.type == "CLOSE-P":
                tokens.selectNext()
            else:
                raise error
        elif tokens.actual.type ==  "CLOSE-P":
            tokens.selectNext()
            return resultado
        else:
            raise error
        return resultado




    def run(origin):
        tokens = Tokenizer(origin)
        resultado = int(Parser.parseExpression(tokens))
        if tokens.actual.type != "EOF":
            raise error
        return resultado
if __name__ == '__main__':
    origin = PrePro.filter(sys.argv[1])   
    result = Parser.run(origin)
    print(result)



        