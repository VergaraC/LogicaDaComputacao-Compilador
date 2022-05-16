from ast import Or
import sys
from os import error
import re

class Token():
    def __init__(self, type,value):
        self.type = type
        self.value = value

class SymbolTable():
    symbolTable = dict()
    def setter(self,var, value, type):
        if var in self.symbolTable.keys():
            if self.symbolTable[var][1] == type:

                ass = list(self.symbolTable[var])
                ass[0] = value
                self.symbolTable[var] = tuple(ass)
                pass
            else:
                raise error
        else:
            raise error
    def getter(self,var):
        if var in self.symbolTable.keys():
            return self.symbolTable[var]
        raise error
    def createVar(self, var, type):
        if var in self.symbolTable.keys():
            raise error
        else:
            self.symbolTable[var] = (None, type)


class Node():
    def __init__(self, value, listNodes):
        self.value = value
        self.children = listNodes
    def Evaluate(self):
        pass

class BinOp(Node):
    def Evaluate(self, symbolTable):
        if self.value == '.':
            return (str(result[0]) + str(result[1]), "STR")

        elif self.children[0].Evaluate(symbolTable)[1] == "INT" and self.children[1].Evaluate(symbolTable)[1] == "INT":
            if self.value == "PLUS":
                return (int(self.children[0].Evaluate(symbolTable)[0]) + int(self.children[1].Evaluate(symbolTable)[0]), "INT")

            elif self.value == "MINUS":
                return (int(self.children[0].Evaluate(symbolTable)[0]) - int(self.children[1].Evaluate(symbolTable)[0]), "INT")

            elif self.value == "MULTIPLICATION":
                return (int(self.children[0].Evaluate(symbolTable)[0]) * int(self.children[1].Evaluate(symbolTable)[0]), "INT")

            elif self.value == "DIVISION":
                return (int(self.children[0].Evaluate(symbolTable)[0]) / int(self.children[1].Evaluate(symbolTable)[0]), "INT")
            
            elif self.value == "AND":
                return (int(self.children[0].Evaluate(symbolTable)[0]) and int(self.children[1].Evaluate(symbolTable)[0]), "INT")
            elif self.value == "OR":
                return (int(self.children[0].Evaluate(symbolTable)[0]) or int(self.children[1].Evaluate(symbolTable)[0]), "INT")
        
        elif self.children[0].Evaluate(symbolTable)[1] == self.children[1].Evaluate(symbolTable)[1]:

            if self.value == "EQUAL":
                if int(self.children[0].Evaluate(symbolTable)[0]) == int(self.children[1].Evaluate(symbolTable)):
                    return (1, "INT")
                else:
                    return (0, "INT")

            elif self.value == "GREATER":
                if int(self.children[0].Evaluate(symbolTable)[0]) > int(self.children[1].Evaluate(symbolTable)):
                    return (1, "INT")
                else:
                    return (0, "INT")

            elif self.value == "LESS":
                if int(self.children[0].Evaluate(symbolTable)[0]) < int(self.children[1].Evaluate(symbolTable)):
                    return (1, "INT")
                else:
                    return (0, "INT")
            else:
                raise error
    
        else:
            raise error
class UnOp(Node):
    def Evaluate(self, symbolTable):
        r = list(self.children[0].Evaluate(symbolTable))
        if r[1] == "INT":
            if self.value == "PLUS":
                return tuple(r)
            elif self.value == "MINUS":
                r[0] = r[0]*(-1)
                return tuple(r)
            elif self.value == "NOT":
                r[0] = not(r[0])
                return tuple(r)
            else:
                raise error
        else:
            raise error
class IntVal(Node):
    def Evaluate(self, symbolTable):
        return (self.value, "INT")
class NoOp(Node):
    def Evaluate(self, symbolTable):
        pass

class Assignement(Node):
    def Evaluate(self, symbolTable):
        symbolTable.createVar(self.children[0].value, "INT")
        symbolTable.setter(self.children[0], self.children[1].Evaluate(symbolTable)[0], self.children[1].Evaluate(symbolTable)[1])
        pass
class Print(Node):
    def Evaluate(self, symbolTable):
        
        print(self.children[0].Evaluate(symbolTable)[0])
        pass
class Scan(Node):
    def Evaluate(self, symbolTable):
        return (int(input()), "INT")
class IfOp(Node):
    def Evaluate(self, symTable):
        if self.children[0].Evaluate(symTable):
            self.children[1].Evaluate(symTable)
        elif len(self.children) == 3:
            self.children[2].Evaluate(symTable)
class WhileOp(Node):
    def Evaluate(self, symTable):
        while self.children[0].Evaluate(symTable):
            self.children[1].Evaluate(symTable)
class VarVal(Node):
    def Evaluate(self, symbolTable):
        return symbolTable.getter(self.value)

class VarDecl(Node):
    def Evaluate(self, symbolTable):
        for i in self.children:
            symbolTable.createVar(i, self.value)
class StrVal(Node):
    def Evaluate(self, symbolTable):
        return (self.value, "STR")
        
class Block(Node):
    def Evaluate(self, symbolTable):
        #print(self.children)
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
        elif self.origin[self.position] == ".":
            self.position+=1
            self.actual = Token("CONCAT","")
            return self.actual
        elif self.origin[self.position] == "(":
            self.position+=1
            self.actual = Token("OPEN-P","")
            return self.actual
        elif self.origin[self.position] == ")":
            self.position+=1
            self.actual = Token("CLOSE-P","")
            return self.actual
        elif self.origin[self.position] == ">":
            self.position+=1
            self.actual = Token("GREATER","")
        elif self.origin[self.position] == "<":
            self.position+=1
            self.actual = Token("LESS","")
        elif self.origin[self.position] == "!":
            self.position+=1
            self.actual = Token("NOT","")
        elif self.origin[self.position] == "|" and self.origin[self.position+1] == "|":
            self.position+=2
            self.actual = Token("OR","")
        elif self.origin[self.position] == "&" and self.origin[self.position+1] == "&":
            self.position+=2
            self.actual = Token("AND","")
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
        elif self.origin[self.position] == ",":
            self.position+=1
            self.actual = Token("COMMA","")
            return self.actual
        elif self.origin[self.position] == "=":
            self.position+=1
            if self.origin[self.position] == "=":
                self.position+=1
                self.actual = Token("EQUAL","")
            else:
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
            elif char == "scanf":
                self.actual = Token("SCAN",char)
            elif char == "if":
                self.actual = Token("IF",char)
            elif char == "else":
                self.actual = Token("ELSE",char)
            elif char == "while":
                self.actual = Token("WHILE",char)
            elif char == "int":
                self.actual = Token("VarType","INT")
            elif char == "string":
                self.actual = Token("VarType","STRING")
            else:
                self.actual = Token("VAR",char)
            return self.actual
        elif self.origin[self.position] == '"':
            self.position += 1
            char = ""
            while self.origin[self.position] != '"' and len(self.origin) > self.position:
                char += self.origin[self.position]
                self.position += 1
            self.position += 1 # tirando " final
            self.actual = Token("STRING",char)

            return self.actual
        else:
            raise error


class PrePro():
    def filter(origin):
        origin = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,origin)
        origin3 = re.sub(' ', '', origin)
        return origin3

class Parser():
    @staticmethod
    def parseTerm(tokens):
        node = Parser.parseFactor(tokens)
        if tokens.actual.type != "MULTIPLICATION" and tokens.actual.type != "DIVISION" and tokens.actual.type != "AND":
            return node
            
        while tokens.actual.type == "MULTIPLICATION" or tokens.actual.type == "DIVISION" or tokens.actual.type == "AND":
            if tokens.actual.type == "MULTIPLICATION":
                node = BinOp("MULTIPLICATION",[node, Parser.parseFactor(tokens)])
            if tokens.actual.type == "DIVISION":
                node = BinOp("DIVISION",[node, Parser.parseFactor(tokens)])
            if tokens.actual.type == "AND":
                node = BinOp("AND",[node, Parser.parseFactor(tokens)])
                
        return node
        
    @staticmethod
    def parseExpression(tokens):
        #print(tokens.actual.type)
        #print(tokens.actual.value)     
        node = Parser.parseTerm(tokens)
        #Parser.tokens.selectNext()
        if tokens.actual.type == "PLUS" or tokens.actual.type == "MINUS" or tokens.actual.type == "EOF" or tokens.actual.type == "CLOSE-P" or tokens.actual.type == "OR" or tokens.actual.type == "CONCAT":
                
            while tokens.actual.type == "PLUS" or tokens.actual.type == "MINUS" or tokens.actual.type == "OR" or tokens.actual.type == "CONCAT":
                if tokens.actual.type == "PLUS":
                    #print("pegou plus")
                    node = BinOp("PLUS",[node, Parser.parseTerm(tokens)])
                    #print(tokens.actual.type)
                    #print(tokens.actual.value)                    
                elif tokens.actual.type == "MINUS":
                    node = BinOp("MINUS",[node, Parser.parseTerm(tokens)])

                elif tokens.actual.type == "OR":
                    node = BinOp("OR",[node, Parser.parseTerm(tokens)])
                elif tokens.actual.type == "CONCAT":
                    node = BinOp("CONCAT",[node, Parser.parseTerm(tokens)])

            
            if tokens.actual.type == "EOF" or tokens.actual.type == "CLOSE-P" or tokens.actual.type == "SEMICOLUM" or tokens.actual.type == "EQUAL":  
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
        #print("startting factor")
        #print(tokens.actual.type)
        #print(tokens.actual.value)
        if tokens.actual.value == "INT":
            node = IntVal(tokens.actual.value,[])
            tokens.selectNext()
            #print(tokens.actual.type)
            #print(tokens.actual.value)
        if tokens.actual.value == "STR":
            node = StrVal(tokens.actual.value,[])
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
        elif tokens.actual.type == "NOT":
            node = UnOp("NOT",[Parser.parseFactor(tokens)])
            #tokens.selectNext()
        elif tokens.actual.type == "SCAN":
            node = Scan("", [])
            tokens.selectNext()
            if tokens.actual.type == "OPEN-P":
                tokens.selectNext()
                if tokens.actual.type == "CLOSE-P":
                    tokens.selectNext()
                else:
                    raise error
            else:
                raise error
        elif tokens.actual.type == "OPEN-P":
            node = Parser.parseRelExpression(tokens)
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
        #print("startting statement")
        #print(tokens.actual.type)
        #print(tokens.actual.value)
        node = None
        
        if tokens.actual.type == "VAR":
            node = VarVal(tokens.actual.value, [])
            tokens.selectNext()
            #print("var ")
            if tokens.actual.type == "ASSINGMENT":
                #print("assigment ")
                #print(tokens.actual.type)
                #print(tokens.actual.value)
                node = Assignement("", [node, Parser.parseRelExpression(tokens)])
                #tokens.selectNext()
                if tokens.actual.type == "SEMICOLUM":
                        #tokens.selectNext()
                        #print(tokens.actual.type)
                        #print(tokens.actual.value)
                        #print("return")
                        return node
                else:
                    raise error
            else:
                raise error
        elif tokens.actual.type == "VARTYPE":
            node = VarDecl(tokens.actual.value, [])
            tokens.selectNext()
            if tokens.actual.type == "VAR":
                node.children.append(tokens.actual.value)
                tokens.selectNext()
                while tokens.actual.type == "COMMA":
                    tokens.selectNext()
                    if tokens.actual.type == "VAR":
                        node.children.append(tokens.actual.value)
                        tokens.selectNext()
                    else:
                        raise error
            else:
                raise error
        elif tokens.actual.type == "PRINT":
            tokens.selectNext()
            if tokens.actual.type == "OPEN-P":
                node = Print("", [Parser.parseRelExpression(tokens)])
                if tokens.actual.type == "CLOSE-P":
                    tokens.selectNext()
                    if tokens.actual.type == "SEMICOLUM": 
                        tokens.selectNext() 
                        return node
                    else:
                        raise error
                else:
                    raise error
            else:
                raise error
        elif tokens.actual.type == "SEMICOLUM":
            tokens.selectNext()
            if(node == None):
                node = NoOp("", [])
            return node
        elif tokens.actual.type == "WHILE":
            tokens.selectNext()
            if tokens.actual.type == "OPEN-P":
                node1 = Parser.parseRelExpression(tokens)
                if tokens.actual.type == "CLOSE-P":
                    tokens.selectNext()
                    node2 = Parser.parseStatement(tokens)
                    node = WhileOp("", [node1,node2])
                    return node
                else:
                    raise error
            else:
                raise error
        elif tokens.actual.type == "IF":
            tokens.selectNext()
            if tokens.actual.type == "OPEN-P":
                node1 = Parser.parseRelExpression(tokens)
                if tokens.actual.type == "CLOSE-P":
                    tokens.selectNext()
                    node2 = Parser.parseStatement(tokens)
                    #print("ff")
                    #print(tokens.actual.type)
                    #print(tokens.actual.value)
                    
                    if tokens.actual.type == "ELSE":
                        tokens.selectNext()
                        node3 = Parser.parseStatement(tokens)
                        node = IfOp("", [node1,node2,node3])
                    else:  
                        node = IfOp("", [node1,node2])
                    return node
                else:
                    raise error
            else:
                raise error
        else:
            #print("pre chamar block")
            #print(tokens.actual.type)
            #print(tokens.actual.value)
            node = Parser.parseBlock(tokens)
            return node

    @staticmethod
    def parseRelExpression(tokens):
        #tokens.selectNext()
        node = Parser.parseExpression(tokens)
        if tokens.actual.type == "EQUAL":
            node = BinOp("EQUAL",[node, Parser.parseExpression(tokens)])
        elif tokens.actual.type == "GREATER":
            node = BinOp("GREATER",[node, Parser.parseExpression(tokens)])
        elif tokens.actual.type == "LESS":
            node = BinOp("LESS",[node, Parser.parseExpression(tokens)])
        else:
            return node
        return node

    @staticmethod
    def parseBlock(tokens):
        #tokens.selectNext()
        ###while tokens.actual.type != "EOF":
            ###tokens.selectNext()
            ###print("T:  ",tokens.actual.type)
        #print(tokens.actual.type)
        #print(tokens.actual.value)
        children = []
        if tokens.actual.type == "OPEN-BR":
            
            tokens.selectNext()
            #print(tokens.actual.type)
            #print(tokens.actual.value)
            while tokens.actual.type != "CLOSE-BR":
                if(tokens.actual.type == "EOF"):
                    raise error
                
                node = Parser.parseStatement(tokens)
                #print("Statement out")
                #print(tokens.actual.type)
                #print(tokens.actual.value)
                children.append(node)
            #print("while out")
            #print(tokens.actual.type)
            #print(tokens.actual.value)
            node = Block("", children)
            tokens.selectNext()
            
        else:
            #print(tokens.actual.type)
            #print(tokens.actual.value)
            raise error
        return node

    def run(origin):
        tokens = Tokenizer(origin)
        tokens.selectNext()
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
    



        