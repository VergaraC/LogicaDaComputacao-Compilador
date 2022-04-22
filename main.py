import sys
from os import error
import re

class Token():
    def __init__(self, type,value):
        self.type = type
        self.value = value

class SymbolTable():
    symbolTable = dict()
    def setter(self,var, value):
        self.symbolTable[var] = value
        pass
    def getter(self,var):
        if var in self.symbolTable.keys():
            return self.symbolTable[var]
        raise error


class Node():
    def __init__(self, value, listNodes):
        self.value = value
        self.children = listNodes
    def Evaluate(self):
        pass

class BinOp(Node):
    def Evaluate(self, symbolTable):
        if self.value == "PLUS":
            return int(self.children[0].Evaluate(symbolTable)) + int(self.children[1].Evaluate(symbolTable))

        elif self.value == "MINUS":
            return int(self.children[0].Evaluate(symbolTable)) - int(self.children[1].Evaluate(symbolTable))

        elif self.value == "MULTIPLICATION":
            return int(self.children[0].Evaluate(symbolTable)) * int(self.children[1].Evaluate(symbolTable))

        elif self.value == "DIVISION":
            return int(self.children[0].Evaluate(symbolTable)) / int(self.children[1].Evaluate(symbolTable))
    
        else:
            raise error
class UnOp(Node):
    def Evaluate(self, symbolTable):
        r = 0
        if self.value == "PLUS":
            r += self.children[0].Evaluate(symbolTable)
            return r
        elif self.value == "MINUS":
            r -= self.children[0].Evaluate(symbolTable)
            return r
        else:
            raise error
class IntVal(Node):
    def Evaluate(self, symbolTable):
        return self.value
class NoOp(Node):
    def Evaluate(self, symbolTable):
        pass

class Assignement(Node):
    def Evaluate(self, symbolTable):
        symbolTable.setter(self.children[0], self.children[1].Evaluate(symbolTable))
        pass
class Print(Node):
    def Evaluate(self, symbolTable):
        print(self.children[0].Evaluate(symbolTable))
        pass
class VarVal(Node):
    def Evaluate(self, symbolTable):
        return symbolTable.getter(self.value)
        
class Block(Node):
    def Evaluate(self, symbolTable):
        for i in self.children:
            i.Evaluate(symbolTable)
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
        
        while (self.origin[self.position] == " " or self.origin[self.position] == "\n" or self.origin[self.position] == "\t" ) and self.position < len(self.origin):
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
        elif self.origin[self.position] == "{":
            self.position+=1
            self.actual = Token("OPEN-BR","")
            return self.actual
        elif self.origin[self.position] == "}":
            self.position+=1
            self.actual = Token("CLOSE-BR","")
            return self.actual
        elif self.origin[self.position] == ";":
            self.position+=1
            self.actual = Token("SEMICOLUM","")
            return self.actual
        elif self.origin[self.position] == "=":
            self.position+=1
            self.actual = Token("ASSINGMENT","")
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

        elif self.origin[self.position].isalpha():
            char = self.origin[self.position]
            self.position += 1
            while self.position < len(self.origin) and (self.origin[self.position].isalnum() or self.origin[self.position] == "_"):
                char += self.origin[self.position]
                self.position += 1
            
            if char == "printf":
                self.actual = Token("PRINT",char)
            else:
                self.actual = Token("VAR",char)
            return self.actual
                
class PrePro():
    def filter(origin):
        origin = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,origin)
        origin3 = re.sub(' ', '', origin)
        return origin3

class Parser():
    @staticmethod
    def parseTerm(tokens):
        node = Parser.parseFactor(tokens)
        if tokens.actual.type != "MULTIPLICATION" and tokens.actual.type != "DIVISION":
            return node
            
        while tokens.actual.type == "MULTIPLICATION" or tokens.actual.type == "DIVISION":
            if tokens.actual.type == "MULTIPLICATION":
                node = BinOp("MULTIPLICATION",[node, Parser.parseFactor(tokens)])
            if tokens.actual.type == "DIVISION":
                node = BinOp("DIVISION",[node, Parser.parseFactor(tokens)])
                
        return node
        
    @staticmethod
    def parseExpression(tokens):

        node = Parser.parseTerm(tokens)
        #Parser.tokens.selectNext()
        if tokens.actual.type == "PLUS" or tokens.actual.type == "MINUS" or tokens.actual.type == "EOF" or tokens.actual.type == "CLOSE-P":
                
            while tokens.actual.type == "PLUS" or tokens.actual.type == "MINUS":
                if tokens.actual.type == "PLUS":
                    print("pegou plus")
                    node = BinOp("PLUS",[node, Parser.parseTerm(tokens)])
                    print(tokens.actual.type)
                    print(tokens.actual.value)
            
                    
                elif tokens.actual.type == "MINUS":
                    node = BinOp("MINUS",[node, Parser.parseTerm(tokens)])

            
            if tokens.actual.type == "EOF" or tokens.actual.type == "CLOSE-P" or tokens.actual.type == "SEMICOLUM":  
                return node
            else:
                print("Error")
                print(tokens.actual.type)
                print(tokens.actual.value)
            
                raise error
        else:
            #print("returnin expression")
            #print(tokens.actual.type)
            #print(tokens.actual.value)
            
            return node

    @staticmethod
    def parseFactor(tokens):
        tokens.selectNext()
        if tokens.actual.type == "NUMBER":
            node = IntVal(tokens.actual.value,[])
            tokens.selectNext()
        elif tokens.actual.type == "VAR":
            node = VarVal(tokens.actual.value,[])
            tokens.selectNext()
        elif tokens.actual.type == "PLUS":
            node = UnOp("PLUS",[Parser.parseFactor(tokens)])
            #tokens.selectNext()
        elif tokens.actual.type == "MINUS":
            node = UnOp("MINUS",[Parser.parseFactor(tokens)])
            #tokens.selectNext()
        elif tokens.actual.type == "OPEN-P":
            node = Parser.parseExpression(tokens)
            if tokens.actual.type == "CLOSE-P":
                tokens.selectNext()
            else:
                raise error
        else:
            #print(tokens.actual.type)
            #print(tokens.actual.value)
            raise error
        return node

    @staticmethod
    def parseStatement(tokens):
        #print(tokens.actual.type)
        #print(tokens.actual.value)
        node = None
        
        if tokens.actual.type == "VAR":
            varName = tokens.actual.value
            tokens.selectNext()
            
            if tokens.actual.type == "ASSINGMENT":
                
                print("assigment ")
                print(tokens.actual.type)
                print(tokens.actual.value)
                node = Assignement("", [varName, Parser.parseExpression(tokens)])
                
            else:
                raise error
        if tokens.actual.type == "PRINT":
            tokens.selectNext()
            #print("dentro do print")
            #print(tokens.actual.type)
            #print(tokens.actual.value)
            if tokens.actual.type == "OPEN-P":
                #okens.selectNext() n precisa pq no expression ele pega
                #print("pre parse")
                #print(tokens.actual.type)
                #print(tokens.actual.value)
                node = Print("", [Parser.parseExpression(tokens)])
                #tokens.selectNext()
                #print("pre closep")
                #print(tokens.actual.type)
                #print(tokens.actual.value)
                if tokens.actual.type == "CLOSE-P":
                    #print("closep")
                    tokens.selectNext()
                    #print(tokens.actual.type)
                    #print(tokens.actual.value)
                    if tokens.actual.type == "SEMICOLUM":
                        tokens.selectNext()
                        #print(tokens.actual.type)
                        #print(tokens.actual.value)
                        #print("return")
                        return node
                    else:
                        raise error
                else:
                    raise error
                
            else:
                raise error
        if tokens.actual.type == "SEMICOLUM":
            tokens.selectNext()
            if(node == None):
                node = NoOp("", [])
            return node
        else:
            print(tokens.actual.type)
            print(tokens.actual.value)
            raise error

    @staticmethod
    def parseBlock(tokens):
        tokens.selectNext()
        ###while tokens.actual.type != "EOF":
            ###tokens.selectNext()
            ###print("T:  ",tokens.actual.type)
        #print(tokens.actual.type)
        #print(tokens.actual.value)
        if tokens.actual.type == "OPEN-BR":
            children = []
            tokens.selectNext()
            #print(tokens.actual.type)
            #print(tokens.actual.value)
            while tokens.actual.type != "CLOSE-BR":
                if(tokens.actual.type == "EOF"):
                    raise error
                
                node = Parser.parseStatement(tokens)
                print("Statement out")
                print(tokens.actual.type)
                print(tokens.actual.value)
                children.append(node)
            #print("while out")
            #print(tokens.actual.type)
            #print(tokens.actual.value)
            node = Block("", children)
            tokens.selectNext()
            return node
        else:
            #print(tokens.actual.type)
            #print(tokens.actual.value)
            raise error

    def run(origin):
        tokens = Tokenizer(origin)
        node = Parser.parseBlock(tokens)
        #resultado = Parser.parseExpression(tokens).Evaluate()
        if tokens.actual.type != "EOF":
            raise error
        symtable = SymbolTable()
        return node.Evaluate(symtable)
if __name__ == '__main__':
    file = sys.argv[1]
    with open(file, "r") as f:
        origin = f.readlines()
        origin1 = "".join(origin)
        origin2 = PrePro.filter(origin1)

        result = Parser.run(origin2)
    



        