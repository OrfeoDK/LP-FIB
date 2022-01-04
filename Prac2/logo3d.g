grammar logo3d;

root : block EOF ;

block : procedureDef* ;

procedureDef : PROC ID OPAR (far=farg car=carg*)? CPAR IS state=statement* END ;

farg : expr ;

carg : COMA expr ;

statement : assignment
    | lectura
    | escritura
    | stateif
    | statewhile
    | statefor
    | procedureCall
    ;

assignment : <assoc=right> ID ASSIGN expr ;

lectura : LEC ID ;

escritura : ESC expr ;

stateif : IF expr THEN statement* (ELSE statement*)? END ;

statewhile : WHILE expr DO statement* END ;

statefor : FOR ID FROM (INT | FLOAT | ID) TO (INT | FLOAT | ID) DO statement* END ;

procedureCall : ID OPAR (far=farg car=carg*)? CPAR ;

expr : expr (MUL | DIV) expr # MultDivExpr
    | expr (SUM | RES) expr # SumResExpr
    | expr (GT | LT | GOE | LOE) expr #relationExpr
    | expr (EQ | NEQ) expr #equalExpr
    | atom #atomExpr
    | '-' (INT | FLOAT) #natomExpr
    ;

atom : (INT | FLOAT) #numberAtom
    | (TRUE | FALSE) #boolAtom
    | ID #idAtom
    ;

MUL : '*';
DIV : '/';
SUM : '+';
RES : '-';

EQ : '==';
NEQ : '!=';
GT : '>';
LT : '<';
GOE : '>=';
LOE : '<=';

TRUE : 'TRUE';
FALSE : 'FALSE';

PROC : 'PROC';
IS : 'IS';

ASSIGN : ':=';

LEC : '>>';
ESC : '<<';

IF : 'IF';
THEN : 'THEN';
ELSE : 'ELSE';
END : 'END';

WHILE : 'WHILE';
DO : 'DO';

FOR : 'FOR';
FROM : 'FROM';
TO : 'TO';

OPAR : '(';
CPAR : ')';
COMA : ',';

INT : [0-9]+ ;
FLOAT : [0-9]+ '.' [0-9]* ;
ID : ('a'..'z' | 'A'..'Z' | '_') ('a'..'z' | 'A'..'Z' | '_' | '0'..'9')* ;

COMENT : '//' ~[\r\n]* -> skip ;

WS : [ \t\r\n]+ -> skip ;
