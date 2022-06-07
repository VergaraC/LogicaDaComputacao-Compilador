from ast import Or
from lib2to3.pgen2 import token
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
        # print("Setter")
        # print(var)
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
class FuncTable():
    funcTable = dict()
    
    def getter(self,var):
        try:
            return tuple(self.funcTable[var])
        except:
            raise error
    def createFunc(self, no, id, type):
        if id in self.funcTable.keys():
            raise error
        else:
            self.funcTable[id] = [no, type]
            

class Node():
    def __init__(self, value, listNodes):
        self.value = value
        self.children = listNodes
    def Evaluate(self):
        pass

class BinOp(Node):
    def Evaluate(self, symbolTable, FuncTable):
        #print("BINOP")
        #print(self.children)
        r1 = self.children[0].Evaluate(symbolTable, FuncTable)
        #print(r1)
        r2 = self.children[1].Evaluate(symbolTable, FuncTable)
        #print(r2)
        #print(self.value)
        # print(self.children[0].Evaluate(symbolTable))
        # print(self.children[1].Evaluate(symbolTable))
        # print(self.children[0].Evaluate(symbolTable))
        # print(self.children[1].Evaluate(symbolTable))
        
        if self.value == "CONCAT":
            return (str(r1[0]) + str(r2[0]), "STR")

        elif r1[1] == "INT" and r2[1] == "INT":
            if self.value == "PLUS":
                return (int(r1[0]) + int(r2[0]), "INT")

            elif self.value == "MINUS":
                return (int(r1[0]) - int(r2[0]), "INT")

            elif self.value == "MULTIPLICATION":
                return (int(r1[0]) * int(r2[0]), "INT")

            elif self.value == "DIVISION":
                return (int(r1[0]) / int(r2[0]), "INT")
            
            elif self.value == "AND":
                return (int(r1[0]) and int(r2[0]), "INT")
            elif self.value == "OR":
                return (int(r1[0]) or int(r2[0]), "INT")
        
        if r1[1] == r2[1]:

            if self.value == "EQUAL":
                if r1[0] == r2[0]:
                    return (1, "INT")
                else:
                    return (0, "INT")

            elif self.value == "GREATER":
                if r1[0] > r2[0]:
                    return (1, "INT")
                else:
                    return (0, "INT")

            elif self.value == "LESS":
                if r1[0] < r2[0]:
                    return (1, "INT")
                else:
                    return (0, "INT")
            else:
                print("ERROR")
                print(self.value)
                print(r1)
                print(r2)
                raise error
    
        else:
            raise error
class UnOp(Node):
    def Evaluate(self, symbolTable, FuncTable):
        #print("UNOP")
        #print(self.value)
        #print(self.children)
        #print("eae")
        r = self.children[0].Evaluate(symbolTable, FuncTable)
        #print(r)
        #print("hm")
        r = list(r)
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
    def Evaluate(self, symbolTable, FuncTable):
        #print("INTVAL")
        return (self.value, "INT")
class NoOp(Node):
    def Evaluate(self, symbolTable, FuncTable):
        #print("NOOP")
        pass

class Assignement(Node):
    def Evaluate(self, symbolTable, FuncTable):
        #print("ASS")
        #print(self.children)
        ass = self.children[1].Evaluate(symbolTable,FuncTable)
        #print(ass[1])
        #print(self.children[0].Evaluate(symbolTable)[1])
        symbolTable.setter(self.children[0].value, ass[0], ass[1])
        pass
class Print(Node):
    def Evaluate(self, symbolTable, FuncTable):
        #print("PRINT")
        a = self.children[0].Evaluate(symbolTable, FuncTable)[0]
        if type(a) is str:
            print(a)
        else:
            print(int(a))
        pass
class Scan(Node):
    def Evaluate(self, symbolTable, FuncTable):
        #print("SCAN")
        return (int(input()), "INT")
class IfOp(Node):
    def Evaluate(self, symTable, FuncTable):
        #print("IF")
        if self.children[0].Evaluate(symTable,  FuncTable)[0]:
            self.children[1].Evaluate(symTable,  FuncTable)
        elif len(self.children) == 3:
            self.children[2].Evaluate(symTable,  FuncTable)
class WhileOp(Node):
    def Evaluate(self, symTable,  FuncTable):
        #print("WHILE")
        while self.children[0].Evaluate(symTable,  FuncTable)[0]:
            self.children[1].Evaluate(symTable,  FuncTable)
class VarVal(Node):
    def Evaluate(self, symbolTable, FuncTable):
        #print("VARVAL")
        return symbolTable.getter(self.value)

class VarDecl(Node):
    def Evaluate(self, symbolTable, FuncTable):
        #print("VARDECL")
        for i in self.children:
            symbolTable.createVar(i, self.value)

class FuncDecl(Node):
    def __init__(self, value, args, block):
        self.value = value
        self.args = args
        self.block = block

    def Evaluate(self, symbolTable, FuncTable):
        #print("FUNCDECL") self, no, id, type):
        FuncTable.createFunc(self, self.value[0], self.value[1])
class FuncCall(Node):
    def __init__(self, value, args):
        self.value = value
        self.args = args
        self.symbolTable = SymbolTable()

    def Evaluate(self, symbolTable, FuncTable):
        func = FuncTable.getter(self.value)
        #print(func)
        #print("FUNCCALL")
        #print(self.args)
        #print(func)
        if len(self.args) == len(func[0].args):
            argsList = list()
            if(len(self.args) == 0):
                return func[0].block.Evaluate(self.symbolTable, FuncTable)
            else:
                for i in func[0].args:
                    i.Evaluate(self.symbolTable, FuncTable)
                    argsList.append(i.children[0].value)
                for local, i2 in zip(self.args, argsList):
                    self.symbolTable.setter(i2,local.Evaluate(symbolTable,FuncTable))
                return func[0].block.Evaluate(self.symbolTable, FuncTable)
        else:
            raise error
class ReturnOp(Node):
    def Evaluate(self, symbolTable, funcTable):
        #print("return")
        return self.child.Evaluate(symbolTable, funcTable)
class StrVal(Node):
    def Evaluate(self, symbolTable, FuncTable):
        #print("STRVAL")
        return (self.value, "STRING")
        
class Block(Node):
    def Evaluate(self, symbolTable, FuncTable):
        #print(self.children)
        #print("BLOCK")
        #print(self.children)
        for i in self.children:
            #print(i)
            if i.value == "return":
                return i.Evaluate(symbolTable, FuncTable)
            i.Evaluate(symbolTable, FuncTable)
            #print("foi")
        pass
class Program(Node):
    
    def Evaluate(self, symbolTable, funcTable):
        #print(self.children)
        for i in self.children:

            i.Evaluate(symbolTable, funcTable)

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
                self.actual = Token("VARTYPE","INT")
            elif char == "str":
                self.actual = Token("VARTYPE","STRING")
            elif char == "void":
                self.actual = Token("VARTYPE","VOID")
            elif char == "return":
                self.actual = Token("RETURN",char)
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
        #origin3 = re.sub(' ', '', origin)
        return origin

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
                # print("Error")
                # print(tokens.actual.type)
                # print(tokens.actual.value)
            
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
        if tokens.actual.type == "NUMBER":
            # print("int")
            node = IntVal(tokens.actual.value,[])
            tokens.selectNext()
            # print(tokens.actual.type)
            # print(tokens.actual.value)
        elif tokens.actual.type == "STRING": ### Sepa vai da merda
            node = StrVal(tokens.actual.value,[])
            tokens.selectNext()
        elif tokens.actual.type == "VAR":
            varVal = tokens.actual.value
            tokens.selectNext()
            if tokens.actual.type == "OPEN-P":
                tokens.selectNext()
                args = list()
                if tokens.actual.type != "CLOSE-P":
                    while tokens.actual.type != "CLOSE-P":
                        args.append(Parser.parseExpression(tokens))
                        if tokens.actual.type == "COMMA":
                            args.append(Parser.parseExpression(tokens))
                            if tokens.actual.type == "CLOSE-P":
                                node = FuncCall(varVal,args)
                            else:
                                raise error
                        else:
                            raise error
                    tokens.selectNext()
                elif tokens.actual.type == "CLOSE-P":
                    node = FuncCall(varVal,args)
                else:
                    raise error
            else:
                node = VarVal(varVal,[])
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
        #print("starting statement")
        #print(tokens.actual.type)
        #print(tokens.actual.value)
        node = None
        #print(tokens.actual.type)
        #print(tokens.actual.value)
        
        if tokens.actual.type == "VAR":
            #print(tokens.actual.type)
            #print(tokens.actual.value)
            node = VarDecl(tokens.actual.value, [])
            tokens.selectNext()
            #print("var ")
            #print(tokens.actual.type)
            #print(tokens.actual.value)
            if tokens.actual.type == "OPEN-P": #pra funct
                tokens.selectNext()
                args = list()
                if tokens.actual.type != "CLOSE-P":
                    while tokens.actual.type != "CLOSE-P":
                        args.append(Parser.parseRelExpression(tokens))
                        if tokens.actual.type == "COMMA":
                            args.append(Parser.parseRelExpression(tokens))
                            if tokens.actual.type == "CLOSE-P":
                                node = FuncCall(node, args)
                            else:
                                raise error
                        else:
                            raise error
                    tokens.selectNext()         
                elif tokens.actual.type == "CLOSE-P":
                    node = FuncCall(node, args)
                    tokens.selectNext()
                else:
                    raise error                
            elif tokens.actual.type == "ASSINGMENT":
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
        elif tokens.actual.type == "RETURN":
            tokens.selectNext()
            if tokens.actual.type == "OPEN-P":
                node = ReturnOp("RETURN", Parser.parseRelExpression(tokens))
                if tokens.actual.type == "CLOSE-P":
                    tokens.selectNext()
                    if tokens.actual.type == "SEMICOLUM":
                        tokens.selectNext()
                    else:
                        raise error
                else:
                    raise error
            else:
                raise error
        elif tokens.actual.type == "VARTYPE":
            #print(tokens.actual.type)
            #print(tokens.actual.value)
            #print("Nova var")
            # print("EAE")
            node = VarDecl(tokens.actual.value, [])
            tokens.selectNext()
            #print("Agora var")
            #print(tokens.actual.type)
            #print(tokens.actual.value)
            if tokens.actual.type == "VAR":
                node.children.append(tokens.actual.value)
                tokens.selectNext()
                #print("agota comma")
                while tokens.actual.type == "COMMA":
                    tokens.selectNext()
                    if tokens.actual.type == "VAR":
                        node.children.append(tokens.actual.value)
                        tokens.selectNext()
                    else:
                        raise error

                if tokens.actual.type == "SEMICOLUM": 
                    tokens.selectNext() 
                    return node
                else:
                    raise error
                   
                #print("saiu while")
            else:
                raise error
            # print("saiu")

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
            # print('NODE')
            # print(node)
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
                    # print("ff")
                    # print(tokens.actual.type)
                    # print(tokens.actual.value)
                    # print("deveria ser else")
                    if tokens.actual.type == "SEMICOLUM":
                        tokens.selectNext()
                        # print(tokens.actual.type)
                        # print(tokens.actual.value)
                        # print("deveria ser else")
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
        # print("saindo Statement")

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
        #while tokens.actual.type != "EOF":
            #tokens.selectNext()
            #print("T:  ",tokens.actual.type)
        #print(tokens.actual.type)
        #print(tokens.actual.value)
        # print("Novo Block")
        # print(tokens.actual.type)
        # print(tokens.actual.value)
        children = []
        if tokens.actual.type == "OPEN-BR":
            
            tokens.selectNext()
            #print(tokens.actual.type)
            #print(tokens.actual.value)
            while tokens.actual.type != "CLOSE-BR":
                if(tokens.actual.type == "EOF"):
                    raise error
                
                node = Parser.parseStatement(tokens)
                # print(node)
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

    @staticmethod
    def parseProgram(tokens):
        node = Program(0,[])
        while tokens.actual.type != "EOF":
            #print(tokens.actual.type)
            #print(tokens.actual.value)
            #a = Parser.parseDeclaration(tokens)
            #print(a)
            node.children.append(Parser.parseDeclaration(tokens))
        node.children.append(FuncCall("main", []))
        return node
    
    @staticmethod
    def parseDeclaration(tokens):
        #print(tokens.actual.type)
        #print(tokens.actual.value)
        if tokens.actual.type == "VARTYPE":
            typeD = tokens.actual.value
            tokens.selectNext()
            
            if tokens.actual.type == "VAR":
                nameD = tokens.actual.value
                tokens.selectNext()
                
                if tokens.actual.type == "OPEN-P":
                    tokens.selectNext()
                    args = list()
                    
                    if tokens.actual.type != "CLOSE-P" :
                        tokens.selectNext()
                        if tokens.actual.type == "VARTYPE":
                            c = tokens.actual.value
                            tokens.selectNext()
                            if tokens.actual.type == "VAR":
                                dec = VarDecl(c,tokens.actual.value)
                                args.append(dec)
                                tokens.selectNext()
                                while tokens.actual.type == "COMMA" :
                                    tokens.selectNext()
                                    if tokens.actual.type == "VARTYPE":
                                        c = tokens.actual.value
                                        tokens.selectNext()
                                        if(tokens.actual.type == "VAR"):
                                            dec = VarDecl(c,tokens.actual.value)
                                            args.append(dec)
                                            tokens.selectNext()
                                        else:
                                            raise error
                                    else:
                                        raise error
                                if tokens.actual.type == "CLOSE-P":
                                    tokens.selecrNext()
                                    node = FuncDecl([nameD,typeD], args, Parser.parseBlock(tokens))
                                    return node
                            else:
                                raise error
                        else:
                            raise error
                    elif tokens.actual.type == "CLOSE-P":
                        tokens.selectNext()
                        node = FuncDecl([nameD,typeD], args, Parser.parseBlock(tokens))
                        return node
                    else:
                        raise error
                else:
                    raise error
            else:
                raise error
        else:
            print(tokens.actual.type)
            print(tokens.actual.value)
            raise error
    def run(origin):
        tokens = Tokenizer(origin)
        tokens.selectNext()
        node = Parser.parseProgram(tokens)
        if tokens.actual.type != "EOF":
            raise error
        symtable = SymbolTable()
        funcTable = FuncTable()
        return node.Evaluate(symtable,funcTable)
if __name__ == '__main__':
    file = sys.argv[1]
    with open(file, "r") as f:
        origin = f.readlines()
        origin1 = "".join(origin)
        origin2 = PrePro.filter(origin1)

        result = Parser.run(origin2)
    



        