grammar pandaQ;

root: statement*;

statement:      (select
                | assignment
                | plot
                )
                ';'
                ;

select: 'select' ('*'|columnList) 'from' ID order? whereCond? join*
        | 'select' ('*'|columnList) 'from' ID whereIn? order? join*
        ;

columnList: (columnName|calculatedColumn) (',' (columnName|calculatedColumn))*;

columnName: identificator;

calculatedColumn: expr 'as' identificator;


expr    : '(' expr ')'                                    # parenthesisBin
        | expr ('*'|'/') expr                             # opBin
        | expr ('+'|'-') expr                             # opBin
        | FLOAT                                           # float
        | INT                                             # int
        | ID                                              # calculatedName
        ;

identificator: ID;


order: 'order by' orderColumnAscDesc (',' orderColumnAscDesc)*;

orderColumnAscDesc: ID ('asc'|'desc')?;


whereCond: 'where' exprBool;

whereIn: 'where' ID 'in' '('select')';

exprBool        : '(' exprBool ')'                        # parenthesisBool
                | exprBool ('<'|'=') exprBool             # opBinBool
                | <assoc=left> 'not' exprBool             # notBool
                | exprBool ('and') exprBool               # opBinBool
                | ID                                      # nameBool
                | INT                                     # intBool
                | FLOAT                                   # floatBool
                ;



join: 'inner join' ID 'on' ID '=' ID;

assignment: ID ':=' select;

plot: 'plot' ID;




INT: [0-9]+;
FLOAT: [0-9]+ '.' [0-9]+;

ID  : [a-zA-Z_][a-zA-Z0-9_]* ;
WS  : [ \t\n\r]+ -> skip ;

