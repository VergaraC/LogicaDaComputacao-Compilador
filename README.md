![git status](http://3.129.230.99/svg/VergaraC/LogicaDaComputacao-Compilador/)
![Diagrama Sintático](DS1.png)
EBNF:

EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = ("+" | "-") FACTOR | "(" EXPRESSION ")" | number ;
