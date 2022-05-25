from ast import Or
import sys
from os import error
import re

from dbus import NameExistsException

class Token():
    def __init__(self, type,value):
        self.type = type
        self.value = value

class Nasm():

    file = sys.argv[1].replace('.c', '.asm')
    def __init__(self):
        with open("header.txt", "r") as h:
            self.assembly = h.read()
        self.footer = "POP EBP \n" + "MOV EAX, 1 \n" +  "INT 0x80 \n"
        pass
    def write(self, text):
        self.assembly += text
        self.assembly += "\n"

    def dump(self):
        f = open(file , "w")
        f.write(self.assembly)
        f.close()

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
            self.symbolTable[var] = (None, type, self.pointer)
            self.pointer += 4


class Node():

    id = 0
    def __init__(self, value, listNodes):
        self.value = value
        self.children = listNodes
        self.id = Node.getId()
    def Evaluate(self):
        pass
    @staticmethod
    def getId():
        Node.id += 1
        return Node.id

class BinOp(Node):
    def Evaluate(self, symbolTable, Nasm):
        #print("BINOP")
        #print(self.children)
        r1 = self.children[0].Evaluate(symbolTable)
        Nasm.write("PUSH EBX")
        #print(r1)
        r2 = self.children[1].Evaluate(symbolTable)
        Nasm.write("POP EAX")
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
        
                Nasm.write("ADD EAX, EBX" + "\n")
                Nasm.write("MOV EBX, EAX" + "\n")

            elif self.value == "MINUS":
                
                Nasm.write("SUB EAX, EBX" + "\n")
                Nasm.write("MOV EBX, EAX" + "\n")

            elif self.value == "MULTIPLICATION":
                
                Nasm.write("IMUL EAX, EBX" + "\n")
                Nasm.write("MOV EBX, EAX" + "\n")

            elif self.value == "DIVISION":
                
                Nasm.write("IDIV EAX, EBX" + "\n")
                Nasm.write("MOV EBX, EAX" + "\n")
            
            elif self.value == "AND":
                
                Nasm.write("AND EAX, EBX" + "\n")
                Nasm.write("MOV EBX, EAX" + "\n")

            elif self.value == "OR":
                
                Nasm.write("ORR EAX, EBX" + "\n")
                Nasm.write("MOV EBX, EAX" + "\n")
        
        if r1[1] == r2[1]:
            
            if self.value == "EQUAL":

                Nasm.write("CMP EAX, EBX" + "\n")
                Nasm.write("CALL binop_je" + "\n")

            elif self.value == "GREATER":
                
                Nasm.write("CMP EAX, EBX" + "\n")
                Nasm.write("CALL binop_jg" + "\n")

            elif self.value == "LESS":
                
                Nasm.write("CMP EAX, EBX" + "\n")
                Nasm.write("CALL binop_jl" + "\n")

            else:
                print("ERROR")
                print(self.value)
                print(r1)
                print(r2)
                raise error
    
        else:
            raise error
class UnOp(Node):
    def Evaluate(self, symbolTable, Nasm):
        #print("UNOP")
        #print(self.value)
        #print(self.children)
        #print("eae")
        r = self.children[0].Evaluate(symbolTable)
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
    def Evaluate(self, symbolTable, Nasm):
        #print("INTVAL")

        Nasm.write("MOV EBX, " + str(self.value) + "\n")
        return (self.value, "INT")
class NoOp(Node):
    def Evaluate(self, symbolTable, Nasm):
        #print("NOOP")
        pass

class Assignement(Node):
    def Evaluate(self, symbolTable, Nasm):
        #print("ASS")
        #print(self.children)
        ass = self.children[1].Evaluate(symbolTable)
        #print(ass[1])
        #print(self.children[0].Evaluate(symbolTable)[1])
        symbolTable.setter(self.children[0].value, ass[0], ass[1])
        get = symbolTable.getter(self.children[0].value)
        Nasm.write("MOV [EBP-" + get[2] + "], EBX \n")
        pass
class Print(Node):
    def Evaluate(self, symbolTable, Nasm):
        #print("PRINT")
        self.children[0].Evaluate(symbolTable)[0]
        Nasm.write("PUSH EBX \n")
        Nasm.write("CALL print \n")
        Nasm.write("POP EBX \n")
        pass
class Scan(Node):
    def Evaluate(self, symbolTable, Nasm):
        #print("SCAN")
        return (int(input()), "INT")
class IfOp(Node):
        
    def Evaluate(self, symTable, Nasm):
        #print("IF")
        idIf = Nasm.getId()
        Nasm.write("IF" + idIf +": \n")
        self.children[0].Evaluate(symTable, Nasm)
        Nasm.write("CMP EBX, False \n")
            
        if len(self.children) == 3:
            Nasm.write("JE ELSE" + idIf + "\n")
            self.children[1].Evaluate(symTable, Nasm)
            Nasm.write("JMP EXIT" + idIf + "\n")
            Nasm.write("ELSE" + idIf + ": \n")
            self.children[2].Evaluate(symTable, Nasm)
        else:
            self.children[1].Evaluate(symTable, Nasm)
            Nasm.write("JE EXIT" + idIf + "\n")
            self.children[1].Evaluate(symTable, Nasm)
            Nasm.write("JMP EXIT" + idIf + "\n")
        Nasm.write("EXIT" +idIf+ ": \n")

class WhileOp(Node):
    def Evaluate(self, symTable, Nasm):
        #print("WHILE")
        idW = Nasm.newId()
        Nasm.write("LOOP" + idW + ": \n")
        self.children[0].Evaluate(symTable, Nasm)
        Nasm.write("CMP EBX, False \n")
        Nasm.write("JE EXIT" + idW + " \n")
        self.children[1].Evaluate(symTable, Nasm)
        Nasm.write("JMP LOOP" + idW + " \n")
        Nasm.write("EXIT" + idW + ": \n")
            
class VarVal(Node):
    def Evaluate(self, symbolTable, Nasm):
        #print("VARVAL")
        get = symbolTable.getter(self.value)
        Nasm.write("MOV EBX, [EBP-" + get[2] + "] +\n")

class VarDecl(Node):
    def Evaluate(self, symbolTable, Nasm):
        #print("VARDECL")
        for i in self.children:
            Nasm.write("PUSH DWORD 0")
            symbolTable.createVar(i, self.value)
class StrVal(Node):
    def Evaluate(self, symbolTable, Nasm):
        #print("STRVAL")
        return (self.value, "STRING")
        
class Block(Node):
    def Evaluate(self, symbolTable, Nasm):
        #print(self.children)
        #print("BLOCK")
        #print(self.children)
        for i in self.children:
            #print(i)
            i.Evaluate(symbolTable)
            #print("foi")
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
                self.actual = Token("VARTYPE","INT")
            elif char == "str":
                self.actual = Token("VARTYPE","STRING")
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
        #print("starting statement")
        #print(tokens.actual.type)
        #print(tokens.actual.value)
        node = None
        #print(tokens.actual.type)
        #print(tokens.actual.value)
        
        if tokens.actual.type == "VAR":
            #print(tokens.actual.type)
            #print(tokens.actual.value)
            node = VarVal(tokens.actual.value, [])
            tokens.selectNext()
            #print("var ")
            #print(tokens.actual.type)
            #print(tokens.actual.value)
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

    def run(origin):
        tokens = Tokenizer(origin)
        tokens.selectNext()
        node = Parser.parseBlock(tokens)
        #resultado = Parser.parseExpression(tokens).Evaluate()
        if tokens.actual.type != "EOF":
            raise error
        symtable = SymbolTable()
        Nasm = Nasm()
        return node.Evaluate(symtable, Nasm)
if __name__ == '__main__':
    file = sys.argv[1]
    with open(file, "r") as f:
        origin = f.readlines()
        origin1 = "".join(origin)
        origin2 = PrePro.filter(origin1)

        result = Parser.run(origin2)
    



        