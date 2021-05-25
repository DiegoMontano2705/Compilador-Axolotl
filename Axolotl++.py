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
from Classes.Memoria import *
from Classes.QuadruplesManager import *
from Classes.TablaManager import *
######################################################################################
#DIRS MEMORIA VIRTUAL
#G=GLOBAL; CTE=CONSTANTE; TMP=TEMPORAL;
#E=ENTERO; F=FLOTANTE; C=CHAR; B=BOOL; 
#INI=INICIA; FIN=TERMINA; 
#Dir Globales 10,000 - 20,4999 
G_E_INI=10000
G_E_FIN=114999
G_F_INI=15000
G_F_FIN=12999
G_C_INI=13000
G_C_FIN=14499
G_TMP_E_INI=14500
G_TMP_E_FIN=15999
G_TMP_F_INI=16000
G_TMP_F_FIN=17499
G_TMP_C_INI=17500
G_TMP_C_FIN=18999
G_TMP_B_INI=19000
G_TMP_B_FIN=20999
#Dir Constantes 20,500 - 21,499
CTE_E_INI=20500
CTE_E_FIN=20999
CTE_F_INI=21000
CTE_F_FIN=21499
#Dir locales 21,500 - 28,499
L_E_INI=21500
L_E_FIN=22499
L_F_INI=22500
L_F_FIN=23499
L_C_INI=23500
L_C_FIN=24499
L_TMP_E_INI=24500
L_TMP_E_FIN=25499
L_TMP_F_INI=25500
L_TMP_F_FIN=26499
L_TMP_C_INI=26500
L_TMP_C_FIN=27499
L_TMP_B_INI=27500
L_TMP_B_FIN=28499
#codigos de operacion
cod_operacion = {
    '+': 1,
    '-': 2,
    '*': 3,
    '/': 4,
    '=': 5,
    '<': 6,
    '>': 7,
    '<=': 8,
    '>=': 9,
    '==': 10,
    '&': 11,
    '|': 12,
    'print': 13,
    'goto': 14,
    'gotof': 15,
    'gosub': 16,
    'endproc': 17,
    'return': 18
}
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


#Building managers
quads = QuadruplesManager()
lex.lex() #Building the lexer
superTabla = TablaManager()
superTabla.crearTabla("global", dirInicio="")
ctes_memoria = Memoria() #crear memoria para constantes
ctes_memoria.setDicsAux("constantes") #Asignar direcciones default
global_memoria = Memoria() #crear memoria para globales
global_memoria.setDicsAux("global") #Asignar direcciones default
######################################################################################
#Grammatic rules
def p_programa(p):
    ''' programa : STARTPROGRAMA ID SEMICOLON main
                | STARTPROGRAMA ID SEMICOLON programaAux main
    '''
    superTabla.set_nombrePrograma(p[2])


def p_main(p):
    ''' main : PRINCIPAL LP RP LCB estatutosAux endprog
    '''

def p_endprog(p):
    ''' endprog : RCB '''
    quads.fillQuadruples() 
    # quads.print_quadruples()

def p_programaAux(p):
    ''' programaAux : clases programaAux
                        | dec_vars programaAux
                        | funcionesAux programaAux
                        | clases
                        | dec_vars
                        | funcionesAux
    '''
######################################################################################
#Declarar Variables

def p_dec_vars(p):
    ''' dec_vars : VARIABLES form_vars
    '''

def p_form_vars(p):
    ''' form_vars : typeAuxId COLON form_vars_aux SEMICOLON form_vars
                    | typeAuxId COLON form_vars_aux SEMICOLON 
    '''

def p_form_vars_aux(p):
    ''' form_vars_aux : ID
                    | ID COMMA form_vars_aux
                    | ID form_vars_aux2
                    | ID form_vars_aux2 COMMA form_vars_aux
    '''
    currTabla = superTabla.get_currentTablaId()
    currType = superTabla.get_currentType()
    superTabla.insertRowToTablaVar(currTabla, p[1], currType, "vars") #agregar var y tipo en su respectiva tabla
    #Guardar variables globales
    if(currTabla == "global"):
        global_memoria.setGlobalVal(p[1], currType, "vars")
    superTabla.addContRecursos(superTabla.get_currentTablaId(), currType) #Contabilizar recursos por funcion/clase

def p_form_vars_aux2(p):
    ''' form_vars_aux2 : LSB CTEI RSB
                        | LSB CTEI COMMA CTEI RSB
    '''
    # print("multi")

def p_typeAuxId(p):
    ''' typeAuxId : tipo'''
    superTabla.set_currentType(p[1]) #Auxiliar para identificar tipo de variable.

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
    #Borrar tabla de vars
    superTabla.set_currentScope("global") #A la hora de salir de la clase, vuleve a estar en un scope global.

#Auxiliar para identificar clase
def p_claseId(p):
    ''' claseId : ID '''
    p[0] = p[1]
    superTabla.crearTabla(p[1], scope="class", dirInicio="", metodosClase="")
    superTabla.set_currentScope("method_"+p[1]) #Reconocer funciones dentro de clase
    superTabla.set_currentTablaId(p[1]) #Reconocer en que clase me encuentro.
    

######################################################################################
#Funciones

def p_funcionesAux(p):
    ''' funcionesAux : funciones
                        | funciones funcionesAux
    '''

def p_funciones(p):
    ''' funciones : funcionIdAux LP RP LCB dec_vars estatutosAux RCB
                    | funcionIdAux LP parametros RP LCB dec_vars estatutosAux RCB
                    | funcionIdAux LP RP LCB estatutosAux RCB
                    | funcionIdAux LP parametros RP LCB estatutosAux RCB
    '''
    # currTabla = superTabla.get_currentTablaId()
    # superTabla.deleteTablaVars(currTabla) #Borrar su tabla de variables
    superTabla.set_currentTablaId("global")

def p_funcionId(p):
    ''' funcionIdAux : tipo_retorno FUNCION ID'''
    #crear memoria
    superTabla.crearTabla(p[3], scope=superTabla.get_currentScope(), retorno=p[1], dirInicio="", pointerParams="", quadIni="")
    superTabla.set_currentTablaId(p[3]) #Reconocer en que tabla se encuentra

######################################################################################
#Tipos variables

def p_tipo(p):
    ''' tipo : tipo_simple
            | tipo_compuesto
    '''
    p[0] = p[1]

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
    p[0] = p[1]

def p_parametros(p):
    ''' parametros : tipo_simple ID
                    | tipo_simple ID COMMA parametros
    '''
    currTabla = superTabla.get_currentTablaId()
    superTabla.insertRowToTablaVar(currTabla, p[2], p[1], "vars") #Agregar var tabla variables
    superTabla.insertRowToListaParms(currTabla, p[1]) #Agregar tipo a lista de parametros

def p_var(p):
    ''' var : idAssignId
            | idAssignId LSB CTEI COMMA CTEI RSB
            | idAssignId LSB CTEI RSB
            | idAssignId POINT ID
    '''

def p_asign_vars(p):
    ''' asign_vars : var equalId exp SEMICOLON
                    | var equalId CTEC SEMICOLON
    '''

#Auxiliar para identificar id de asignacion.
def p_idAssignId(p):
    ''' idAssignId : ID '''
    p[0] = p[1]
    tipoVar = superTabla.getTipoIdTablaVars(superTabla.get_currentTablaId(), p[1])
    print(tipoVar)
    if(superTabla.get_currentTablaId()!="global"):
        dirVar = superTabla.getDirIdTablaVars(superTabla.get_currentTablaId(),p[1]) 
        #Checar en tabla global
    else:
        #get tipo var
        dirVar = global_memoria.getDirMemory(str(p[1]))
    quads.id_push(p[1], tipoVar) #Agregar id con varTipo
    # print(p[1])
    # quads.id_push(dirVar, tipoVar) #Agregar dirs con varTipo

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
    ''' decision : IF LP exp startIf THEN LCB estatutosAux endIf_Else
                | IF LP exp startIf THEN LCB estatutosAux startElse LCB estatutosAux endIf_Else
    '''

def p_startIf(p):
    ''' startIf : RP '''
    quads.operator_push('GoToF')
    quads.pilaSaltos.put(quads.getID()-1)

def p_endIf_Else(p):
    ''' endIf_Else : RCB '''
    end = quads.pilaSaltos.pop()
    nxtQuad = quads.getID()
    quads.quadruples[end].setResult(nxtQuad)

def p_startElse(p):
    ''' startElse : ELSE '''
    quads.operator_push('GoTo')
    false = quads.pilaSaltos.pop()
    quads.pilaSaltos.put(quads.getID()-1)
    quads.quadruples[false].setResult(quads.getID())


def p_rep_condicional(p):
    ''' rep_condicional : MIENTRAS startWhile exp startWhile2 HACER LCB estatutosAux endWhile
    '''

def p_startWhile(p):
    ''' startWhile : LP '''
    quads.pilaSaltos.put(quads.getID())

def p_startWhile2(p):
    ''' startWhile2 : RP '''
    quads.operator_push('GoToF')
    quads.pilaSaltos.put(quads.getID()-1)

def p_endWhile(p):
    ''' endWhile : RCB '''
    end = quads.pilaSaltos.pop()
    ret = quads.pilaSaltos.pop()
    quads.operator_push('GoTo')
    quads.quadruples[quads.getID() - 1].setResult(ret)
    quads.quadruples[end].setResult(quads.getID())


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

def p_f(p): #lpid y rpid para identificar ().
    ''' f : lpId exp rpId 
            | ctei
            | ctef
            | ctec
            | var
            | llamada_fun_exp
    '''
    p[0] = p[1]


#Auxiliares identificadores expresion
def p_equalId(p):
    ''' equalId : EQUAL '''
    # print("=")
    quads.operator_push("=")

def p_plusId(p):
    ''' plusId : PLUS '''
    # print("+")
    quads.operator_push("+")


def p_minusId(p):
    ''' minusId : MINUS '''
    # print("-")
    quads.operator_push("-")

def p_timesId(p):
    ''' timesId : TIMES '''
    # print("*")
    quads.operator_push("*")

def p_divideId(p):
    ''' divideId : DIVIDE '''
    # print("/")
    quads.operator_push("/")

def p_greaterThanId(p):
    ''' greaterThanId : GREATER_THAN '''
    # print(">")
    quads.operator_push(">")

def p_greaterEqualThanId(p):
    ''' greaterEqualThanId : GREATER_EQUAL_THAN '''
    # print(">=")
    quads.operator_push(">=")

def p_smallerThanId(p):
    ''' smallerThanId : SMALLER_THAN '''
    # print("<")
    quads.operator_push("<")

def p_smallerEqualThanid(p):
    ''' smallerEqualThanId : SMALLER_EQUAL_THAN '''
    # print("<=")
    quads.operator_push("<=")

def p_isequalId(p):
    ''' isequalId : IS_EQUAL '''
    # print("==")
    quads.operator_push("==")

def p_differentId(p):
    ''' differentId : DIFFERENT '''
    # print("!=")
    quads.operator_push("!=")

def p_lpId(p):
    ''' lpId : LP '''
    # print("(")
    quads.operator_push("(")

def p_rpId(p):
    ''' rpId : RP '''
    # print(")")
    quads.operator_push(")")
######################################################################################
#Constantes
def p_ctei(p):
    ''' ctei : CTEI '''
    p[0] = p[1]
    ctes_memoria.setConstante(int(p[1])) #Agregar a memoria
    dirAux = ctes_memoria.getDirMemory(int(p[1]))
    quads.id_push(p[1], "entero") #Agregar a quads operations
    # print(p[1])
    # quads.id_push(dirAux, "entero") #Agregar dir a quads operations

    
def p_ctef(p):
    ''' ctef : CTEF '''
    p[0] = p[1]
    ctes_memoria.setConstante(float(p[1])) #Agregar a memoria
    dirAux = ctes_memoria.getDirMemory(float(p[1]))
    quads.id_push(p[1], "float") #Agregar a quads operations
    # print(p[1])
    # quads.id_push(dirAux, "float") #Agregar dir a quads opeartions

def p_ctec(p):
    ''' ctec : CTEC '''
    p[0] = p[1]
    ctes_memoria.setConstante(str(p[1])) #Agregar a memoria
    dirAux = ctes_memoria.getDirMemory(str(p[1]))
    quads.id_push(p[1], "char") #Agregar a quads operations
    # quads.id_push(dirAux, "char") #Agrega dir a quads operations

######################################################################################
#Manejo errores
def p_error(p):
    token = f"{p.type}({p.value}) en linea {p.lineno}"
    print(f"Error de sintaxis: error {token}")
    sys.exit()

######################################################################################
#Crear ejecutable .obj
def crearOutFile():
    print("Generando archivo .out ...")
    original_stdout = sys.stdout #Referencia original standar output
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    root = ROOT_DIR+"/Testing/objFiles/"
    nombreProg = superTabla.get_nombrePrograma() 
    with open(root+nombreProg+".out", 'w') as f:
        sys.stdout = f #cambiar standar output to the file
        # print ctes in file
        print("### CTES ###")
        for key, value in ctes_memoria.getMemory().items():
            print(key,value)
        #print quads in file
        print("### QUADS ###")
        listaQuads = quads.getListaQuads()
        for i in range(len(listaQuads)):
            #print con codigo de operacion
            # print("%s %s %s %s %s" % (listaQuads[i].getID(), cod_operacion[listaQuads[i].getOperator()] ,listaQuads[i].getLeftOp(),listaQuads[i].getRightOp(), listaQuads[i].getResult()))
            print("%s %s %s %s %s" % (listaQuads[i].getID(), listaQuads[i].getOperator(),listaQuads[i].getLeftOp(),listaQuads[i].getRightOp(), listaQuads[i].getResult()))
        #print 
        sys.stdout = original_stdout #resete standar output
######################################################################################
#Creating praser
yacc.yacc()
if __name__ == '__main__':
    if (len(sys.argv)>1):
        fileName = sys.argv[1]
        try:
            ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
            namef = ROOT_DIR+"/Testing/axFiles/"+fileName 
            file = open(namef,'r')
            s = file.read()
            file.close()
        except EOFError:
            quit()
    yacc.parse(s) #Parser with grammar
    crearOutFile() #generar ejecutable

######################################################################################
#print testing
# ctes_memoria.printMemory()
# global_memoria.printMemory()
# print(superTabla.getRecursos("global"))
superTabla.printDirFun() #superTabla con funciones/clases/methodos
# superTabla.printTablaVars("global")
# superTabla.printTablaVars("pruebaUno")
# superTabla.printTablaVars("pruebaDos")
# superTabla.printTablaVars("regresaValores")
# superTabla.printTablaVars("creando")
# superTabla.printListaParms("pruebaDos")

