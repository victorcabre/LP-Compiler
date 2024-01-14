grammar pandaQ;

root: statement*;

statement:      select
                | assignment
                ;

select: 'select' ('*'|columnList) 'from' ID order? where? join*;

columnList: (columnName|calculatedColumn) (',' (columnName|calculatedColumn))*;

columnName: identificator;

calculatedColumn: expr 'as' identificator;


expr    : expr ('*'|'/') expr                             # opBin
        | expr ('+'|'-') expr                             # opBin
        | FLOAT                                           # float
        | INT                                             # int
        | ID                                              # calculatedName
        ;

identificator: ID;


order: 'order by' orderColumnAscDesc (',' orderColumnAscDesc)*;

orderColumnAscDesc: ID ('asc'|'desc')?;


where: 'where' exprBool;


exprBool        : exprBool ('<'|'='|'and') exprBool       # opBinBool
                | <assoc=right> 'not' exprBool                          # notBool
                | ID                                      # nameBool
                | INT                                     # intBool
                | FLOAT                                   # floatBool
                ;



join: 'inner join' ID 'on' ID '=' ID;


assignment: ID ':=' select;



INT: [0-9]+;
FLOAT: [0-9]+ '.' [0-9]+;

ID  : [a-zA-Z_][a-zA-Z0-9_]* ;
WS  : [ \t\n\r]+ -> skip ;

