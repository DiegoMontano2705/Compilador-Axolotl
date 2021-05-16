# 
#     Axolotl++: parser & lexer.
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez 
# 

import sys
import os
import ply.lex as lex 
import ply.yacc as yacc
from Classes.QuadruplesManager import *
from Classes.TablaManager import *

######################################################################################
#Tokens
tokens = [
    'PLUS','MINUS','TIMES','DIVIDE',
    'ID','EQUAL','GREATER_THAN', 'GREATER_EQUAL_THAN', 'SMALLER_THAN', 'SMALLER_EQUAL_THAN', 'IS_EQUAL','AND','OR',
    'DIFFERENT','LP','RP','LCB','RCB','LSB','RSB',
    'CTEI','CTEF','CTEC','COMMA','POINT','SEMICOLON','COLON', 'STRING', 'COMMENT',
]

######################################################################################
#Regular Expressions for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUAL = r'='
t_DIFFERENT = r'!='
t_GREATER_THAN = r'>'
t_GREATER_EQUAL_THAN = r'>='
t_SMALLER_THAN = r'<'
t_SMALLER_EQUAL_THAN = r'<='
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

######################################################################################
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

#Building managers
quadruples = QuadruplesManager()
superTabla = TablaManager()

######################################################################################
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
######################################################################################
#Declarar Variables
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

######################################################################################
# Definicion clases
def p_clases(p):
    ''' clases : CLASE claseId LCB RCB SEMICOLON
                | CLASE claseId LCB ATRIBUTOS form_vars RCB SEMICOLON
                | CLASE claseId LCB METODOS funcionesAux RCB SEMICOLON
                | CLASE claseId LCB ATRIBUTOS form_vars METODOS funcionesAux RCB SEMICOLON
                | CLASE claseId SMALLER_THAN HEREDA ID GREATER_THAN LCB RCB SEMICOLON
                | CLASE claseId SMALLER_THAN HEREDA ID GREATER_THAN LCB ATRIBUTOS form_vars RCB SEMICOLON
                | CLASE claseId SMALLER_THAN HEREDA ID GREATER_THAN LCB METODOS funcionesAux RCB SEMICOLON
                | CLASE claseId SMALLER_THAN HEREDA ID GREATER_THAN LCB ATRIBUTOS form_vars METODOS funcionesAux RCB SEMICOLON
    '''
    superTabla.set_currentTablaId("global") #A la hora de salir de la clase, vuleve a estar en un scope global.

#Auxiliar para identificar clase
def p_claseId(p):
    ''' claseId : ID '''
    p[0] = p[1]
    superTabla.crearTabla("class_"+p[1], dirInicio="", recursos=[1,2,3], metodosClase="")
    superTabla.set_currentTablaId("class_"+p[1])

######################################################################################
#Funciones

def p_funcionesAux(p):
    ''' funcionesAux : funciones
                        | funciones funcionesAux
    '''

## Checa esta padre, esta diferente a los diagramas sobre todo la parte de los semicolons
## SOLUCIONADO
def p_funciones(p):
    ''' funciones : funcionIdAux LP RP dec_vars LCB estatutosAux RCB
                    | funcionIdAux LP parametros RP dec_vars LCB estatutosAux RCB
                    | funcionIdAux LP RP LCB estatutosAux RCB
                    | funcionIdAux LP parametros RP LCB estatutosAux RCB
    '''

def p_funcionId(p):
    ''' funcionIdAux : tipo_retorno FUNCION ID'''
    if 'class_' in superTabla.get_currentTablaId(): #Si esta dentro de clase, es method.
        print("funcion dentro clase") #Agregar tabla de funcion en tabla methodos.
    else:
        superTabla.crearTabla(p[3], retorno=p[1], dirInicio="", recursos=[1,2,3], pointerParams="")
        superTabla.set_currentTablaId(p[3])

######################################################################################
#Tipos variables

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
    p[0] = p[1]

def p_tipo_retorno(p):
    ''' tipo_retorno : tipo_simple
                    | VOID
    '''
    p[0] = p[1]

def p_tipo_compuesto(p):
    ''' tipo_compuesto : ID
    '''

def p_parametros(p):
    ''' parametros : tipo_simple ID
                    | tipo_simple ID COMMA parametros
    '''

def p_var(p):
    ''' var : idAssignId
            | idAssignId LSB CTEI COMMA CTEI RSB
            | idAssignId LSB CTEI RSB
            | idAssignId POINT ID
    '''
    # print(p[1])

def p_asign_vars(p):
    ''' asign_vars : var equalId exp SEMICOLON
                    | var equalId CTEC SEMICOLON
    '''

#Auxiliar para identificar id de asignacion.
def p_idAssignId(p):
    ''' idAssignId : ID '''
    p[0] = p[1]

######################################################################################
#Estatutos

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

######################################################################################
#Condicionales

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

######################################################################################
#Expresiones

def p_exp(p):
    ''' exp : OR
            | t_exp
    ''' 
    p[0] = p[1]

def p_t_exp(p):
    ''' t_exp : AND
                | g_exp
    '''
    p[0] = p[1]

def p_g_exp(p):
    ''' g_exp : m_exp greaterThanId m_exp
            | m_exp greaterEqualThanId
            | m_exp smallerThanId m_exp
            | m_exp smallerEqualThanId m_exp
            | m_exp isequalId m_exp
            | m_exp differentId m_exp
            | m_exp
    '''

def p_m_exp(p):
    ''' m_exp : t
                | t m_exp2 
    '''
    p[0] = p[1]

def p_m_exp2(p):
    ''' m_exp2 : plusId m_exp
                | minusId m_exp
    '''

def p_t(p):
    ''' t : f 
          | f t2
    '''
    p[0] = p[1]

def p_t2(p):
    ''' t2 : timesId t
            | divideId t
    '''

#def p_f(p):
#    ''' f : f2
#            | PLUS f2
#            | MINUS f2
#            | TIMES f2
#            | DIVIDE f2 
#    '''
#    print(p[1])


def p_f(p): #lpid y rpid para identificar ().
    ''' f : lpId exp rpId 
            | ctei
            | ctef
            | ctec
            | var
            | llamada_fun_exp
    '''
    p[0] = p[1]
    # if(p[1]): #si no esta vacio
    #     print(p[1])


#Auxiliares identificadores expresion
def p_equalId(p):
    ''' equalId : EQUAL '''
    # print("=")

def p_plusId(p):
    ''' plusId : PLUS '''
    # print("+")

def p_minusId(p):
    ''' minusId : MINUS '''
    # print("-")

def p_timesId(p):
    ''' timesId : TIMES '''
    # print("*")

def p_divideId(p):
    ''' divideId : DIVIDE '''
    # print("/")

def p_greaterThanId(p):
    ''' greaterThanId : GREATER_THAN '''
    # print(">")

def p_greaterEqualThanId(p):
    ''' greaterEqualThanId : GREATER_EQUAL_THAN '''
    # print(">=")

def p_smallerThanId(p):
    ''' smallerThanId : SMALLER_THAN '''
    # print("<")

def p_smallerEqualThanid(p):
    ''' smallerEqualThanId : SMALLER_EQUAL_THAN '''
    # print("<=")

def p_isequalId(p):
    ''' isequalId : IS_EQUAL '''
    # print("==")

def p_differentId(p):
    ''' differentId : DIFFERENT '''
    # print("!=")

def p_lpId(p):
    ''' lpId : LP '''
    # print("(")

def p_rpId(p):
    ''' rpId : RP '''
    # print(")")

def p_ctei(p):
    ''' ctei : CTEI '''
    p[0] = p[1]
    # (p,'i')

def p_ctef(p):
    ''' ctef : CTEF '''
    p[0] = p[1]
    # (p,'f')

def p_ctec(p):
    ''' ctec : CTEC '''
    p[0] = p[1]
    # (p,'c')

######################################################################################
#Manejo errores
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
    namef = ROOT_DIR+"/Testing/test.txt" 
    file = open(namef,'r')
    s = file.read()
    file.close()
except EOFError:
    quit()
#Prase file using own grammar
yacc.parse(s)

#print testing
superTabla.printDirFun()

print("El codigo fue admitido")