#---
# Axochitlt++ Praser
#---
import sys
import ply.lex as lex 
import ply.yacc as yacc

#Inicital tokens
tokens = [
    'PLUS','MINUS','TIMES','DIVIDE',
    'ID','EQUAL','GREATER_THAN','SMALLER_THAN','IS_EQUAL','AND','OR',
    'DIFFERENT','LP','RP','LCB','RCB','LSB','RSB',
    'CTEI','CTEF','CTEC','COMMA','POINT','SEMICOLON','COLON', 'STRING'
]

#Regular Expressions for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUAL = r'\='
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
    'principal' : 'PRINCIPAL',
    '%%' : 'COMMENT',
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

#To ignore whitespaces in code file
t_ignore = r' '

def t_error(t):
    print("Error en caracter '%s' " % t.value[0])
    t.lexer.skip(1)

# Building the lexer
lex.lex()

#Grammatic rules
def p_programa(p):
    ''' programa : STARTPROGRAMA ID SEMICOLON programaAux PRINCIPAL LP RP LCB estatutos RCB
                | comentario STARTPROGRAMA ID SEMICOLON programaAux comentario PRINCIPAL LP RP LCB estatutos RCB
                | comentario STARTPROGRAMA ID SEMICOLON programaAux PRINCIPAL LP RP LCB estatutos RCB
                | STARTPROGRAMA ID SEMICOLON programaAux comentario PRINCIPAL LP RP LCB estatutos RCB
                | STARTPROGRAMA ID SEMICOLON comentario PRINCIPAL LP RP LCB estatutos RCB
                | comentario STARTPROGRAMA ID SEMICOLON PRINCIPAL LP RP LCB estatutos RCB
    '''
def p_comentario(p):
    ''' comentario : COMMENT comentarioPalabras COMMENT
    '''
def p_comentarioPalabras(p):
    ''' comentarioPalabras : CTEC
                            | CTEC comentarioPalabras
    '''
def p_programaAux(p):
    ''' programaAux : clases dec_vars funciones
                    | clases funciones
                    | clases dec_vars
                    | dec_vars funciones
                    | clases
                    | dec_vars
                    | funciones
    '''

def p_dec_vars(p):
    ''' dec_vars : VARIABLES form_vars
                | comentario VARIABLES form_vars
    '''

def p_form_vars(p):
    ''' form_vars : ID COLON tipo SEMICOLON
                    | ID form_vars_aux COLON tipo SEMICOLON
                    | ID form_vars_aux COLON tipo SEMICOLON comentario
    '''

def p_form_vars_aux(p):
    ''' form_vars_aux : COMMA dec_vars
                        | LSB CTEI RSB
                        | LSB CTEI COMMA CTEI RSB
    '''

def p_clases(p):
    ''' clases : CLASE ID LCB RCB SEMICOLON
                | CLASE ID LCB ATRIBUTOS form_vars RCB SEMICOLON
                | CLASE ID LCB METODOS funciones RCB SEMICOLON
                | CLASE ID LCB ATRIBUTOS form_vars METODOS funciones RCB SEMICOLON
                | CLASE ID SMALLER_THAN HEREDA ID GREATER_THAN LCB RCB SEMICOLON
                | CLASE ID SMALLER_THAN HEREDA ID GREATER_THAN LCB ATRIBUTOS form_vars RCB SEMICOLON
                | CLASE ID SMALLER_THAN HEREDA ID GREATER_THAN LCB METODOS funciones RCB SEMICOLON
                | CLASE ID SMALLER_THAN HEREDA ID GREATER_THAN LCB ATRIBUTOS form_vars METODOS funciones RCB SEMICOLON
                | comentario CLASE ID LCB RCB SEMICOLON
                | comentario CLASE ID LCB ATRIBUTOS form_vars RCB SEMICOLON
                | comentario CLASE ID LCB METODOS funciones RCB SEMICOLON
                | comentario CLASE ID LCB ATRIBUTOS form_vars METODOS funciones RCB SEMICOLON
                | comentario CLASE ID SMALLER_THAN HEREDA ID GREATER_THAN LCB RCB SEMICOLON
                | comentario CLASE ID SMALLER_THAN HEREDA ID GREATER_THAN LCB ATRIBUTOS form_vars RCB SEMICOLON
                | comentario CLASE ID SMALLER_THAN HEREDA ID GREATER_THAN LCB METODOS funciones RCB SEMICOLON
                | comentario CLASE ID SMALLER_THAN HEREDA ID GREATER_THAN LCB ATRIBUTOS form_vars METODOS funciones RCB SEMICOLON
    '''

def p_funciones(p):
    ''' funciones : tipo_retorno FUNCION ID LP RP SEMICOLON LCB RCB SEMICOLON LCB estatutos RCB
            | tipo_retorno FUNCION ID LP parametros RP SEMICOLON LCB RCB SEMICOLON dec_vars LCB estatutos RCB
            | tipo_retorno FUNCION ID LP parametros RP SEMICOLON LCB RCB SEMICOLON LCB estatutos RCB
            | tipo_retorno FUNCION ID LP RP SEMICOLON LCB RCB SEMICOLON dec_vars LCB estatutos RCB
            | comentario tipo_retorno FUNCION ID LP RP SEMICOLON LCB RCB SEMICOLON LCB estatutos RCB
            | comentario tipo_retorno FUNCION ID LP parametros RP SEMICOLON LCB RCB SEMICOLON dec_vars LCB estatutos RCB
            | comentario tipo_retorno FUNCION ID LP parametros RP SEMICOLON LCB RCB SEMICOLON LCB estatutos RCB
            | comentario tipo_retorno FUNCION ID LP RP SEMICOLON LCB RCB SEMICOLON dec_vars LCB estatutos RCB
    '''

def p_tipo(p):
    ''' tipo : tipo_simple
            | tipo_compuesto
    '''

def p_tipo_simple(p):
    ''' tipo_simple : INT
                    | FLOAT
                    | CHAR
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
    ''' escritura : PRINT LP exp RP SEMICOLON
                    | PRINT LP STRING RP SEMICOLON
                    | PRINT LP exp COMMA escrituraAux RP SEMICOLON
                    | PRINT LP STRING COMMA escrituraAux RP SEMICOLON
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

def p_estatutosAux(p):
    ''' estatutosAux : estatutos
                        | estatutos estatutosAux
    '''

def p_rep_condicional(p):
    ''' rep_condicional : MIENTRAS LP exp RP HACER LCB estatutosAux RCB
    '''

def p_rep_no_condicional(p):
    ''' rep_no_condicional : DESDE ID EQUAL exp HASTA exp HACER LCB estatutosAux RCB
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
                    | comentario
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
    ''' m_exp : PLUS
                | MINUS
                | t
    '''

def p_t(p):
    ''' t : TIMES
            | DIVIDE
            | f
    '''

def p_f(p):
    ''' f : LP exp RP
            | CTEI
            | CTEF
            | CTEC
            | var
            | llamada_fun
    '''


def p_error(p):
    token = f"{p.type}({p.value}) en linea {p.lineno}"
    print(f"Error de sintaxis: error {token}")
    #print("Error de sintaxis : '%s' " % p.value)
    exit()


#Creating praser
yacc.yacc()

#to check if file exists
try:
    namef = "PLY_Axochitl/fail.txt" 
    file = open(namef,'r')
    s = file.read()
    file.close()
except EOFError:
    quit()
#Prase file using own grammar
yacc.parse(s)
print("El codigo fue admitido")