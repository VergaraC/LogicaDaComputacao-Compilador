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