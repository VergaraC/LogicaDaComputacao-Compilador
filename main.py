import sys
from os import error
import re

class Token():
    def __init__(self, type,value):
        self.type = type
        self.value = value

class Node():
    def __init__(self, value, listNodes):
        self.value = value
        self.children = listNodes
    def Evaluate(self):
        pass

class BinOp(Node):
    def Evaluate(self):
        if self.value == "PLUS":
            return int(self.children[0].Evaluate()) + int(self.children[1].Evaluate())

        elif self.value == "MINUS":
            return int(self.children[0].Evaluate()) - int(self.children[1].Evaluate())

        elif self.value == "MULTIPLICATION":
            return int(self.children[0].Evaluate()) * int(self.children[1].Evaluate())

        elif self.value == "DIVISION":
            return int(self.children[0].Evaluate()) / int(self.children[1].Evaluate())
        else:
            raise error
class UnOp(Node):
    def Evaluate(self):
        r = 0
        if self.value == "PLUS":
            r += self.children[0].Evaluate(self.children[0])
            return r
        elif self.value == "MINUS":
            r -= self.children[0].Evaluate(self.children[0])
            return r
        else:
            raise error
class IntVal(Node):
    def Evaluate(self):
        return self.value
class NoOp(Node):
    def Evaluate(self):
        pass
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
        node = Parser.parseFactor(tokens)
        if tokens.actual.type != "MULTIPLICATION" and tokens.actual.type != "DIVISION":
            return node
            
        while tokens.actual.type == "MULTIPLICATION" or tokens.actual.type == "DIVISION":
            if tokens.actual.type == "MULTIPLICATION":
                node = BinOp("MULTIPLICATION",[node, Parser.parseFactor(tokens)])
                #resultado *= int(Parser.parseFactor(tokens))
            if tokens.actual.type == "DIVISION":
                node = BinOp("DIVISION",[node, Parser.parseFactor(tokens)])

                #resultado /= Parser.parseFactor(tokens)
                
        return node
        
    @staticmethod
    def parseExpression(tokens):

        node = Parser.parseTerm(tokens)
        #Parser.tokens.selectNext()
        if tokens.actual.type == "PLUS" or tokens.actual.type == "MINUS" or tokens.actual.type == "EOF" or tokens.actual.type == "CLOSE-P":
                
            while tokens.actual.type == "PLUS" or tokens.actual.type == "MINUS":
                if tokens.actual.type == "PLUS":
                    node = BinOp("PLUS",[node, Parser.parseTerm(tokens)])
                    #resultado += Parser.parseTerm(tokens)
                    
                elif tokens.actual.type == "MINUS":
                    node = BinOp("MINUS",[node, Parser.parseTerm(tokens)])
                    #resultado -= Parser.parseTerm(tokens)

            
            if tokens.actual.type == "EOF" or tokens.actual.type == "CLOSE-P":  
                return node.Evaluate()
            else:
                raise error
        else:
            raise error

    @staticmethod
    def parseFactor(tokens):
        tokens.selectNext()
        resultado = 0
        if tokens.actual.type == "NUMBER":
            node = IntVal(tokens.actual.value,[])
            #resultado = tokens.actual.value
            tokens.selectNext()
        elif tokens.actual.type == "PLUS":
            node = UnOp("PLUS",[Parser.parseFactor(tokens)])
            #resultado += Parser.parseFactor(tokens)
        elif tokens.actual.type == "MINUS":
            node = UnOp("MINUS",[Parser.parseFactor(tokens)])
            #resultado -= Parser.parseFactor(tokens)
        elif tokens.actual.type == "OPEN-P":
            node = Parser.parseExpression(tokens)
            if tokens.actual.type == "CLOSE-P":
                tokens.selectNext()
            else:
                raise error
        else:
            raise error
        return node




    def run(origin):
        tokens = Tokenizer(origin)
        resultado = int(Parser.parseExpression(tokens))
        if tokens.actual.type != "EOF":
            raise error
        return resultado
if __name__ == '__main__':
    f = open(sys.argv[1],"r")
    origin1 = f.read()
    f.close()
    origin2 = PrePro.filter(origin1)

    result = Parser.run(origin2)
    print(result)



        