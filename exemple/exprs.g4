// Gramàtica per expressions senzilles
grammar exprs;
root : statement*             // l'etiqueta ja és root
     ;

statement : VAR '=' expr                              # assignacio
          | 'write' expr                               # write
          | 'if' expr 'then' statement 'end'       # condicional
          ;

expr : <assoc=right> expr '^' expr                     # opBin
     | expr ('*'|'/') expr                             # opBin
     | expr ('+'|'-') expr                             # opBin
     | expr ('=='|'!='|'>'|'>='|'<'|'<=') expr         # opBin
     | NUM                                             # numero
     | VAR                                             # variable
     ;
NUM : [0-9]+ ;
VAR : [a-z]+ ;
WS  : [ \t\n\r]+ -> skip ;