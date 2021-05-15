#---
# Axolotl++ Praser
#---
import sys
import os
import ply.lex as lex 
import ply.yacc as yacc

#Inicital tokens
tokens = [
    'PLUS','MINUS','TIMES','DIVIDE',
    'ID','EQUAL','GREATER_THAN','SMALLER_THAN','IS_EQUAL','AND','OR',
    'DIFFERENT','LP','RP','LCB','RCB','LSB','RSB',
    'CTEI','CTEF','CTEC','COMMA','POINT','SEMICOLON','COLON', 'STRING', 'COMMENT',
]

#Regular Expressions for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUAL = r'='
t_DIFFERENT = r'!='
t_GREATER_THAN = r'>'
t_SMALLER_THAN = r'<'
t_IS_EQUAL = r'=='
t_AND = r'\&'
t_OR = r'\|'

t_LP = r'\('
t_RP = r'\)'
t_LCB = r'\{'
t_RCB = r'\}'
t_LSB = r'\['
t_RSB = r'\]'
t_COMMA = r','
t_POINT = r'\.'
t_SEMICOLON = r';'
t_COLON = r':'
t_CTEI = r'[0-9]+'
t_CTEF = r'[0-9]+\.[0-9]+'
t_CTEC = r'"([^\\"\n]+|\\.)"'
t_STRING = r'"([^\\"\n]+|\\.)*"'

reserved = {
    'si' : 'IF',
    'entonces' : 'THEN',
    'sino' : 'ELSE',
    'escribe' : 'PRINT',
    'lee' : 'READ',
    'variables' : 'VARIABLES',
    'programa' : 'STARTPROGRAMA',
    'entero' : 'INT',
    'flotante':'FLOAT',
    'char' : 'CHAR',
    'bool' : 'BOOL',
    'principal' : 'PRINCIPAL',
    'void' : 'VOID',
    'regresa' : 'RETURN',
    'atributos' : 'ATRIBUTOS',
    'hereda' : 'HEREDA',
    'metodos' : 'METODOS',
    'clase' : 'CLASE',
    'funcion' : 'FUNCION',
    'mientras' : 'MIENTRAS',
    'hasta' : 'HASTA',
    'hacer' : 'HACER',
    'desde' : 'DESDE',
}

#Adding reserved words to tokens
tokens = tokens + list(reserved.values())

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Error en caracter '%s' " % t.value[0])
    t.lexer.skip(1)

def t_COMMENT(t):
    r'\%%.*'
    pass
    # No return value. Token discarded

#To ignore whitespaces in code file
#t_ignore = r' '
t_ignore=' \t\r\n\f\v' 

# Building the lexer
lex.lex()

#Grammatic rules
def p_programa(p):
    ''' programa : STARTPROGRAMA ID SEMICOLON main
                | STARTPROGRAMA ID SEMICOLON programaAux main
    '''
def p_main(p):
    ''' main : PRINCIPAL LP RP LCB estatutosAux RCB
    '''

def p_programaAux(p):
    ''' programaAux : clases programaAux
                        | dec_vars programaAux
                        | funciones programaAux
                        | clases
                        | dec_vars
                        | funciones
    '''

#### Declarar Variables
def p_dec_vars(p):
    ''' dec_vars : VARIABLES form_vars
    '''

def p_form_vars(p):
    ''' form_vars : tipo COLON form_vars_aux SEMICOLON form_vars
                    | tipo COLON form_vars_aux SEMICOLON 
    '''

def p_form_vars_aux(p):
    ''' form_vars_aux : ID
                    | ID COMMA form_vars_aux
                    | ID form_vars_aux2
                    | ID form_vars_aux2 COMMA form_vars_aux
    '''
def p_form_vars_aux2(p):
    ''' form_vars_aux2 : LSB CTEI RSB
                        | LSB CTEI COMMA CTEI RSB
    '''
####### 

def p_clases(p):
    ''' clases : CLASE ID LCB RCB SEMICOLON
                | CLASE ID LCB ATRIBUTOS form_vars RCB SEMICOLON
                | CLASE ID LCB METODOS funcionesAux RCB SEMICOLON
                | CLASE ID LCB ATRIBUTOS form_vars METODOS funcionesAux RCB SEMICOLON
                | CLASE ID SMALLER_THAN HEREDA ID GREATER_THAN LCB RCB SEMICOLON
                | CLASE ID SMALLER_THAN HEREDA ID GREATER_THAN LCB ATRIBUTOS form_vars RCB SEMICOLON
                | CLASE ID SMALLER_THAN HEREDA ID GREATER_THAN LCB METODOS funcionesAux RCB SEMICOLON
                | CLASE ID SMALLER_THAN HEREDA ID GREATER_THAN LCB ATRIBUTOS form_vars METODOS funcionesAux RCB SEMICOLON
    '''
def p_funcionesAux(p):
    ''' funcionesAux : funciones
                        | funciones funcionesAux
    '''

## Checa esta padre, esta diferente a los diagramas sobre todo la parte de los semicolons
## SOLUCIONADO
def p_funciones(p):
    ''' funciones : tipo_retorno FUNCION ID LP RP dec_vars LCB estatutosAux RCB
                    | tipo_retorno FUNCION ID LP parametros RP dec_vars LCB estatutosAux RCB
                    | tipo_retorno FUNCION ID LP RP LCB estatutosAux RCB
                    | tipo_retorno FUNCION ID LP parametros RP LCB estatutosAux RCB
    '''

def p_tipo(p):
    ''' tipo : tipo_simple
            | tipo_compuesto
    '''

def p_tipo_simple(p):
    ''' tipo_simple : INT
                    | FLOAT
                    | CHAR
                    | BOOL
    '''

def p_tipo_retorno(p):
    ''' tipo_retorno : tipo_simple
                    | VOID
    '''

def p_parametros(p):
    ''' parametros : tipo_simple ID
                    | tipo_simple ID COMMA parametros
    '''

def p_tipo_compuesto(p):
    ''' tipo_compuesto : ID
    '''

def p_var(p):
    ''' var : ID
            | ID LSB CTEI COMMA CTEI RSB
            | ID LSB CTEI RSB
            | ID POINT ID
    '''

def p_asign_vars(p):
    ''' asign_vars : var EQUAL exp SEMICOLON
                    | var EQUAL CTEC SEMICOLON
    '''

def p_llamada_fun(p):
    ''' llamada_fun : ID LP RP SEMICOLON
                    | ID LP exp RP SEMICOLON
    '''

# Para uso en operaciones
def p_llamada_fun_exp(p):
    ''' llamada_fun_exp : ID LP RP 
                    | ID LP exp RP 
    '''

def p_retorno_fun(p):
    ''' retorno_fun :  RETURN LP exp RP SEMICOLON
    '''

def p_lectura(p):
    ''' lectura : READ LP var RP SEMICOLON
            | READ LP var COMMA lecturaaux SEMICOLON
    '''

def p_lecturaaux(p):
    ''' lecturaaux : var
                    | var COMMA lecturaaux
    '''
def p_escritura(p):
    ''' escritura : PRINT LP escrituraAux RP SEMICOLON
    '''

def p_escrituraAux(p):
    ''' escrituraAux : exp
                    | STRING
                    | exp COMMA escrituraAux
                    | STRING COMMA escrituraAux
    '''

def p_decision(p):
    ''' decision : IF LP exp RP THEN LCB estatutosAux RCB
                | IF LP exp RP THEN LCB estatutosAux RCB ELSE LCB estatutosAux RCB
    '''

def p_rep_condicional(p):
    ''' rep_condicional : MIENTRAS LP exp RP HACER LCB estatutosAux RCB
    '''

def p_rep_no_condicional(p):
    ''' rep_no_condicional : DESDE ID EQUAL exp HASTA exp HACER LCB estatutosAux RCB
    '''

def p_estatutosAux(p):
    ''' estatutosAux : estatutos
                        | estatutos estatutosAux
    '''

def p_estatutos(p):
    ''' estatutos : asign_vars
                    | llamada_fun
                    | lectura
                    | escritura
                    | decision
                    | rep_condicional
                    | retorno_fun
                    | rep_no_condicional
                    | dec_vars
    '''

def p_exp(p):
    ''' exp : OR
            | t_exp
    ''' 

def p_t_exp(p):
    ''' t_exp : AND
                | g_exp
    '''

def p_g_exp(p):
    ''' g_exp : m_exp GREATER_THAN m_exp
            | m_exp SMALLER_THAN m_exp
            | m_exp IS_EQUAL m_exp
            | m_exp DIFFERENT m_exp
            | m_exp
    '''

def p_m_exp(p):
    ''' m_exp : t
                | t m_exp2 
    '''

def p_m_exp2(p):
    ''' m_exp2 : PLUS m_exp
                | MINUS m_exp
    '''
    #print(p[1])

def p_t(p):
    ''' t : f 
          | f t2
    '''
    p[0] = p[1]

def p_t2(p):
    ''' t2 : TIMES t
            | DIVIDE t
    '''
    print(p[1],p[2])

#def p_f(p):
#    ''' f : f2
#            | PLUS f2
#            | MINUS f2
#            | TIMES f2
#            | DIVIDE f2 
#    '''
#    print(p[1])

def p_f(p):
    ''' f : LP exp RP
            | ctei
            | ctef
            | ctec
            | var
            | llamada_fun_exp
    '''
    if len(p) <= 2:
        p[0] = p[1]

def p_ctei(p):
    ''' ctei : CTEI '''
    (p,'i')

def p_ctef(p):
    ''' ctef : CTEF '''
    (p,'f')

def p_ctec(p):
    ''' ctec : CTEC '''
    (p,'c')

def p_error(p):
    token = f"{p.type}({p.value}) en linea {p.lineno}"
    print(f"Error de sintaxis: error {token}")
    #print("Error de sintaxis : '%s' " % p.value)
    exit()


#Creating praser
yacc.yacc()

#to check if file exists
try:
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    namef = ROOT_DIR+"/Testing/test1.txt" 
    file = open(namef,'r')
    s = file.read()
    file.close()
except EOFError:
    quit()
#Prase file using own grammar
yacc.parse(s)
print("El codigo fue admitido")