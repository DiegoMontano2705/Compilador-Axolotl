/* 
    Gramatica Team++
    Compiladores
    Diego Fernando Montaño Pérez
    Jose Alberto Gonzalez 
*/

grammar teamplusplus;

//Tokens
PROGRAMA : 'programa';
STRING: '"' ('\\' ["\\] | ~["\\\r\n])* '"';
ID: ([A-Z]|[a-z]) ([A-Z]|[a-z]|[0-9])*;
PLUS: '+';
MINUS: '-';
TIMES: '*';
DIV: '/';
VARIABLES: 'variables';
IF: 'si';
THEN: 'entonces';
ELSE: 'sino';
WHITESPACE : [ \t\r\n]+ -> skip ;
EQUAL: '=';
DIFF: '!=';
GREATER: '>';
SMALLER: '<';
IS_EQUAL: '==';
AND: '&';
OR: '|';
LP: '(';
RP: ')';
LCB: '{';
RCB: '}';
READ: 'lee';
PRINT: 'escribe';
CTEC: ([A-Z]|[a-z]|[0-9]|EQUAL|AND|OR|LP|RP|LCB|RCB|POINT|COMMA|SEMICOLON|COLON|LSB|RSB); 
CTEI: ('0'|([1-9]([0-9])*));
CTEF: ('0'|([1-9]([0-9])*))'.'([0-9]+)(('e'|'E')('+'|'-')?('0'|([1-9]([0-9])*)))? ;
POINT: '.';
COMMA: ',';
SEMICOLON: ';';
COLON: ':';
LSB: '[';
RSB: ']';
INT: 'entero';
FLOAT: 'floatante';
CHAR: 'char';
PRINCIPAL: 'principal';
COMMENT: '%%';
ATRIBUTOS: 'atributos';
HEREDA: 'hereda';
METODOS: 'metodos';
CLASE: 'clase';
FUNCION: 'funcion';
VOID: 'void';
RETURN: 'regresa';
MIENTRAS: 'mientras';
HASTA: 'hasta';
HACER: 'hacer';
DESDE: 'desde';

//Gramatic Rules
programa
: PROGRAMA ID SEMICOLON programaAux PRINCIPAL LP RP LCB estatutos RCB
| comentario PROGRAMA ID SEMICOLON programaAux comentario PRINCIPAL LP RP LCB estatutos RCB
| comentario PROGRAMA ID SEMICOLON programaAux PRINCIPAL LP RP LCB estatutos RCB
| PROGRAMA ID SEMICOLON programaAux comentario PRINCIPAL LP RP LCB estatutos RCB;

comentario
: COMMENT comentarioPalabras COMMENT;

comentarioPalabras
: CTEC comentarioPalabras
| CTEC;

programaAux
: clases dec_vars funciones
| clases funciones
| clases dec_vars
| dec_vars funciones
| clases
| dec_vars
| funciones;

dec_vars
: VARIABLES form_vars
| comentario VARIABLES form_vars;

form_vars
: ID COLON tipo SEMICOLON
| ID form_vars_aux COLON tipo SEMICOLON
| ID form_vars_aux COLON tipo SEMICOLON comentario;

form_vars_aux
: COMMA dec_vars
| LSB CTEI RSB
| LSB CTEI COMMA CTEI RSB;

clases
: CLASE ID LCB RCB SEMICOLON
| CLASE ID LCB ATRIBUTOS form_vars RCB SEMICOLON
| CLASE ID LCB METODOS funciones RCB SEMICOLON
| CLASE ID LCB ATRIBUTOS form_vars METODOS funciones RCB SEMICOLON
//
| CLASE ID SMALLER HEREDA ID GREATER LCB RCB SEMICOLON
| CLASE ID SMALLER HEREDA ID GREATER LCB ATRIBUTOS form_vars RCB SEMICOLON
| CLASE ID SMALLER HEREDA ID GREATER LCB METODOS funciones RCB SEMICOLON
| CLASE ID SMALLER HEREDA ID GREATER LCB ATRIBUTOS form_vars METODOS funciones RCB SEMICOLON
//
| comentario CLASE ID LCB RCB SEMICOLON
| comentario CLASE ID LCB ATRIBUTOS form_vars RCB SEMICOLON
| comentario CLASE ID LCB METODOS funciones RCB SEMICOLON
| comentario CLASE ID LCB ATRIBUTOS form_vars METODOS funciones RCB SEMICOLON
// 
| comentario CLASE ID SMALLER HEREDA ID GREATER LCB RCB SEMICOLON
| comentario CLASE ID SMALLER HEREDA ID GREATER LCB ATRIBUTOS form_vars RCB SEMICOLON
| comentario CLASE ID SMALLER HEREDA ID GREATER LCB METODOS funciones RCB SEMICOLON
| comentario CLASE ID SMALLER HEREDA ID GREATER LCB ATRIBUTOS form_vars METODOS funciones RCB SEMICOLON;

funciones
: tipo_retorno FUNCION ID LP RP SEMICOLON LCB RCB SEMICOLON LCB estatutos RCB
| tipo_retorno FUNCION ID LP parametros RP SEMICOLON LCB RCB SEMICOLON dec_vars LCB estatutos RCB
| tipo_retorno FUNCION ID LP parametros RP SEMICOLON LCB RCB SEMICOLON LCB estatutos RCB
| tipo_retorno FUNCION ID LP RP SEMICOLON LCB RCB SEMICOLON dec_vars LCB estatutos RCB
//with comments
| comentario tipo_retorno FUNCION ID LP RP SEMICOLON LCB RCB SEMICOLON LCB estatutos RCB
| comentario tipo_retorno FUNCION ID LP parametros RP SEMICOLON LCB RCB SEMICOLON dec_vars LCB estatutos RCB
| comentario tipo_retorno FUNCION ID LP parametros RP SEMICOLON LCB RCB SEMICOLON LCB estatutos RCB
| comentario tipo_retorno FUNCION ID LP RP SEMICOLON LCB RCB SEMICOLON dec_vars LCB estatutos RCB;

tipo
: tipo_simple
| tipo_compuesto;

tipo_simple
: INT
| FLOAT
| CHAR;

tipo_retorno
: tipo_simple
| VOID;

parametros
: tipo_simple ID
| tipo_simple ID COMMA parametros;

tipo_compuesto
: ID;

var
: ID
| ID LSB CTEI COMMA CTEI RSB
| ID LSB CTEI RSB
| ID POINT ID;

asign_vars
: var EQUAL exp SEMICOLON
| var EQUAL CTEC SEMICOLON;

llamada_fun
: ID LP RP SEMICOLON
| ID LP exp RP SEMICOLON;

retorno_fun
: RETURN LP exp RP SEMICOLON;

lectura
: READ LP var RP SEMICOLON
| READ LP var COMMA lecturaaux SEMICOLON;

lecturaaux
: var
| var COMMA lecturaaux;

escritura
: PRINT LP exp RP SEMICOLON
| PRINT LP STRING RP SEMICOLON
| PRINT LP exp COMMA escrituraAux RP SEMICOLON
| PRINT LP STRING COMMA escrituraAux RP SEMICOLON;

escrituraAux
: exp
| STRING
| exp COMMA escrituraAux
| STRING COMMA escrituraAux;

decision
: IF LP exp RP THEN LCB estatutosAux RCB
| IF LP exp RP THEN LCB estatutosAux RCB ELSE LCB estatutosAux RCB;

estatutosAux
: estatutos
| estatutos estatutosAux; 

rep_condicional
: MIENTRAS LP exp RP HACER LCB estatutosAux RCB;

rep_no_condicional
: DESDE ID EQUAL exp HASTA exp HACER LCB estatutosAux RCB;

estatutos
: asign_vars
| llamada_fun
| lectura
| escritura
| decision
| rep_condicional
| retorno_fun
| rep_no_condicional
| comentario;

exp
: m_exp GREATER m_exp
| m_exp SMALLER m_exp
| m_exp IS_EQUAL m_exp
| m_exp DIFF m_exp
| m_exp;

m_exp
: PLUS
| MINUS
| t;

t
: TIMES
| DIV
| f;

f
: LP exp RP
| CTEI
| CTEF
| CTEC
| var
| llamada_fun;






