import sys
from os import error

arg = sys.argv[1]
arg =arg.replace(" ","")
i = 0
resultado = 0
nAtual = ""
listaOrdem = list()

while i< len(arg):
    if arg[i].isnumeric():
        nAtual = nAtual + arg[i]      
        
    elif arg[i] == "+" or arg[i] == "-":
        if nAtual != "":
            listaOrdem.append(nAtual)
        listaOrdem.append(arg[i])
        nAtual = ""
    else:
        raise error

    i+=1
if nAtual != "":
    listaOrdem.append(nAtual)
if ("+" not in listaOrdem) and ("-" not in listaOrdem):
    raise error
if listaOrdem[0] == "+" or listaOrdem[0] == "-"  or listaOrdem[len(listaOrdem)-1] == "+" or listaOrdem[len(listaOrdem)-1] == "-":
    raise error
j = 1
resultado = int(listaOrdem[0])
while j< len(listaOrdem):
    if j< len(listaOrdem) - 1:
        notLast = 1
    else:
        notLast = 0
    if listaOrdem[j] == "+":
        resultado += int(listaOrdem[j+1])
        if notLast:
            if not(listaOrdem[j+1].isnumeric()) and notLast:
                raise error
    elif listaOrdem[j] == "-":
        resultado -= int(listaOrdem[j+1])
        if notLast:
            if not(listaOrdem[j+1].isnumeric()):
                raise error
    else:
        if notLast:
            if listaOrdem[j+1].isnumeric():
                raise error
    j+=1
print(resultado)


########################################################################

class Token():
    def __init__(self, type,value):
        self.type = type
        self.value = value
class Tokenizer():
    def __init__(self):
        self.origin = sys.argv[1]
        self.position = 0
        self.actual = None
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
                self.actual = Token("NUMBER",int(algarismos))
                return self.actual
        else:
            raise error


        

class Parser():
    tokens = None
    result = 0
    def parseExpession():
        tokens = Tokenizer()
        token = tokens.selectNext()
        if token.type == "NUMBER":
            result = token.value()
            token = tokens.selectNext()
                
            while token.type == "PLUS" or token.type == "MINUS":
            
                if token.type == "PLUS":
                    token = tokens.selectNext()
                    if token.type == "NUMBER":
                        result += token.value()
                    else:
                        raise error
                if token.type == "MINUS":
                    token = tokens.selectNext()
                    if token.type == "NUMBER":
                        result -= token.value()
                    else:
                        raise error
            
                token = tokens.selectNext()
            return result
        else:
            return error
        