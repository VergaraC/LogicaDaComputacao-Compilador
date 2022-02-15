import sys
from os import error

arg = sys.argv[1]
arg =arg.replace(" ","")
i = 0
resultado = 0
nAtual = ""
listaOrdem = list()
listaAlgarismos = ["0","1","2","3","4","5","6","7","8","9"]
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

if listaOrdem[0] == "+" or listaOrdem[0] == "-"  or listaOrdem[len(listaOrdem)-1] == "+" or listaOrdem[len(listaOrdem)-1] == "-":
    raise error
j = 1
resultado = int(listaOrdem[0])
while j< len(listaOrdem):
   
    if listaOrdem[j] == "+":
        resultado += int(listaOrdem[j+1])
    elif listaOrdem[j] == "-":
        resultado -= int(listaOrdem[j+1])
    j+=1
print(resultado)