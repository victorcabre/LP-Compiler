grammar pandaQ;

root: statement*;

statement: select;

select: 'select' ('*'|columnList)'from' ID;

columnList: (identificator|calculatedColumn) (',' (identificator|calculatedColumn))*;

columnName: identificator;

calculatedColumn: expression 'as' identificator;


expression      : identificator
                | operation
                ;

operation :;




identificator: ID;

ID  : [a-zA-Z_][a-zA-Z0-9_]* ;
WS  : [ \t\n\r]+ -> skip ;

