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
#codigos de operacion
cod_operacion = {
    '+': 1,
    '-': 2,
    '*': 3,
    '/': 4,
    '<': 5,
    '>': 6,
    '<=': 7,
    '>=': 8,
    '==': 9,
    '&': 10,
    '|': 11,
    '=': 12,
    'Print': 13,
    'Read': 14,
    'GoTo': 15,
    'GoToF': 16,
    'GoSub': 17,
    'Return': 18,
    'Era' : 19,
    'EndFunc' : 20,
    'Param' : 21,
    'endprog': 22
}
######################################################################################
#Tokens
tokens = [
    'PLUS','MINUS','TIMES','DIVIDE',
    'ID','EQUAL','GREATER_THAN', 'GREATER_EQUAL_THAN', 'SMALLER_THAN', 'SMALLER_EQUAL_THAN', 'IS_EQUAL','AND','OR',
    'DIFFERENT','LP','RP','LCB','RCB','LSB','RSB',
    'CTEI','CTEF','CTEC','COMMA','POINT','SEMICOLON','COLON', 'STRING', 
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
#t_CTEC = r'"([^\\"\n]+|\\.)"'
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

def t_CTEC(t):
    r'\'[\w]\''
    t.value = str(t.value)
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
superTabla.crearTabla("global", dirInicio=None)
ctes_memoria = Memoria() #crear memoria para constantes
ctes_memoria.setDicsAux("constantes") #Asignar direcciones default
global_memoria = Memoria() #crear memoria para globales
global_memoria.setDicsAux("global") #Asignar direcciones default

######################################################################################
#Grammatic rules
def p_programa(p):
    ''' programa : startProg ID SEMICOLON main
                | startProg ID SEMICOLON programaAux main
    '''
    #                | startProg ID SEMICOLON dec_vars programaAux main
    superTabla.setListaTemporales("global", quads.getRecursosTmpsGlobales()) #Asignar temporales globales usados en el programa
    superTabla.set_nombrePrograma(p[2]) #Nombre del programa
    superTabla.deleteTablaVars("global") #Borrar tabla variables globales
    quads.setEndProg() #Agregar end of program.

def p_startProg(p):
    ''' startProg : STARTPROGRAMA '''
    quads.operator_push('GoTo')

def p_main(p):
    ''' main : startmain LP RP LCB estatutosAux endprog
    '''
def p_startmain(p):
    ''' startmain : PRINCIPAL '''
    quads.quadruples[0].setResult(quads.getID())

def p_endprog(p):
    ''' endprog : RCB '''
    quads.fillQuadruples() 

def p_programaAux(p):
    ''' programaAux : clases programaAux
                        | dec_vars programaAux
                        | funciones programaAux
                        | clases
                        | funciones
                        | dec_vars
    '''
######################################################################################
#Declarar Variables

def p_dec_vars(p):
    ''' dec_vars : VARIABLES form_vars
    '''
    
def p_form_vars(p):
    ''' form_vars : typeAuxId COLON form_vars_aux SEMICOLON
    '''

def p_form_vars_aux(p):
    ''' form_vars_aux : ID
                    | ID COMMA form_vars_aux
                    | ID form_vars_aux2
                    | ID form_vars_aux2 COMMA form_vars_aux
    '''
    currTabla = superTabla.get_currentTablaId()
    currType = superTabla.get_currentType()
    # print(currTabla, p[1], currType, "vars")
    superTabla.insertRowToTablaVar(currTabla, p[1], currType, "vars") #agregar var y tipo en su respectiva tabla
    #Guardar variables globales
    if(currTabla == "global"):
        global_memoria.setGlobalVal(p[1], currType, "vars")
    superTabla.addContRecursos(superTabla.get_currentTablaId(), currType) #Contabilizar recursos por funcion/clase
    
def p_form_vars_aux2(p):
    ''' form_vars_aux2 : LSB CTEI RSB
                        | LSB CTEI COMMA CTEI RSB
    '''

def p_typeAuxId(p):
    ''' typeAuxId : tipo'''
    superTabla.set_currentType(p[1]) #Auxiliar para identificar tipo de variable.
    #print(p[1])

######################################################################################
# Definicion clases
def p_clases(p):
    ''' clases : CLASE claseId LCB RCB SEMICOLON
                | CLASE claseId LCB ATRIBUTOS form_vars RCB SEMICOLON
                | CLASE claseId LCB METODOS funciones RCB SEMICOLON
                | CLASE claseId LCB ATRIBUTOS form_vars METODOS funciones RCB SEMICOLON
    '''
    #Borrar tabla de vars
    currTabla = superTabla.get_currentTablaId()
    superTabla.setListaTemporales(currTabla, quads.getRecursosTmpsLocales()) #set recursos tmps utilizados
    quads.setCurrTabla("global")
    superTabla.set_currentScope("global") #A la hora de salir de la clase, vuleve a estar en un scope global.

#Auxiliar para identificar clase
def p_claseId(p):
    ''' claseId : ID '''
    p[0] = p[1]
    superTabla.crearTabla(p[1], scope="class", metodosClase=None)
    superTabla.set_currentScope("method_"+p[1]) #Reconocer funciones dentro de clase
    superTabla.set_currentTablaId(p[1]) #Reconocer en que clase me encuentro.
    quads.setCurrTabla(p[1])
    

######################################################################################
#Funciones

def p_funciones(p):
    ''' funciones : funcionIdAux LP RP LCB estatutosAux endFunction
                    | funcionIdAux LP parametros RP LCB estatutosAux endFunction
    '''
    currTabla = superTabla.get_currentTablaId()
    superTabla.setListaTemporales(currTabla, quads.getRecursosTmpsLocales())
    superTabla.setListaParms(currTabla) #Asignar orden correcto de parametros.
    superTabla.deleteTablaVars(currTabla) #Borrar su tabla de variables
    superTabla.set_currentTablaId("global")
    quads.setCurrTabla("global")
    

def p_endFunction(p):
    ''' endFunction : RCB '''
    quads.operator_push('EndFunc')

def p_funcionIdAux(p):
    ''' funcionIdAux : tipo_retorno FUNCION ID'''
    #crear memoria
    superTabla.crearTabla(p[3], scope=superTabla.get_currentScope(), retorno=p[1], dirInicio=None, pointerParams=None, quadIni= quads.getID()+1)
    superTabla.set_currentTablaId(p[3]) #Reconocer en que tabla se encuentra
    quads.setCurrTabla(p[3])


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
    #checar si es un objeto de Clase
    try:
        if(superTabla.getScopeFun(p[1]) != "class"):
            print("Error:", p[1], "no tipo valido.")
            sys.exit()
    except:
        print("Error:", p[1], "no es nombre de clase.")

def p_parametros(p):
    ''' parametros : tipo_simple ID
                    | tipo_simple ID COMMA parametros
    '''
    currTabla = superTabla.get_currentTablaId()
    superTabla.addContRecursos(superTabla.get_currentTablaId(), p[1]) #Contabilizar recursos por funcion/clase
    superTabla.insertRowToTablaVar(currTabla, p[2], p[1], "vars") #Agregar var tabla variables
    superTabla.insertRowToListaParms(currTabla, p[1]) #Agregar tipo a lista de parametros


def p_var(p):
    ''' var : idAssignId
            | idAssignId LSB CTEI COMMA CTEI RSB
            | idAssignId LSB CTEI RSB
            | objetoAtributo
    '''
    
def p_objetoAtributo(p):
    ''' objetoAtributo : idAssignId POINT ID'''
    #manejar direcciones objetos
    currTabla = superTabla.get_currentTablaId()
    currTipo = superTabla.get_currentType()
    if(currTabla!="global"): #local
        dirObjeto = superTabla.getDirIdTablaVars(currTabla,p[1]) 
    else: #global
        dirObjeto, _ = global_memoria.getDirMemory(str(p[1]))
    #direccion para el atributo dentro de la clase.
    dirAtributo = superTabla.getDirIdTablaVars(currTipo,p[3])
    #checar tipo del atributo
    tipoAtributo = superTabla.getTipoIdTablaVars(currTipo, p[3])
    quads.id_push(str(dirObjeto)+"_"+str(dirAtributo), tipoAtributo)

def p_asign_vars(p):
    ''' asign_vars : var equalId llamada_fun asignend 
                    | var equalId exp asignend SEMICOLON 
                    | var equalId CTEC asignend SEMICOLON 
    '''

def p_asignend(p):
    ''' asignend : '''
    quads.fillQuadruples()

#Auxiliar para identificar id de asignacion.
def p_idAssignId(p):
    ''' idAssignId : ID '''
    p[0] = p[1]
    currTabla = superTabla.get_currentTablaId()
    currTipo = superTabla.get_currentType()
    #Solo cuando no son objetos.
    if(currTipo in ["entero", "flotante", "char", "bool", None]):
        #Validar que exista y extraer tipo.
        if(currTabla !="global"): 
            #checar si es metodo y de que clase
            currScope = superTabla.getScopeFun(currTabla)
            if("method_" in currScope): #es un metodo de clase.
                nomClase = currScope.replace("method_", "")
                dirVar = superTabla.getDirIdTablaVars(nomClase,p[1]) 
                tipoVar = superTabla.getTipoIdTablaVars(nomClase, p[1])
            else:
                dirVar = superTabla.getDirIdTablaVars(superTabla.get_currentTablaId(),p[1]) 
                tipoVar = superTabla.getTipoIdTablaVars(superTabla.get_currentTablaId(), p[1])
                if(dirVar == -1): #Si no esta local, buscar global
                    dirVar, tipoVar = global_memoria.getDirMemory(str(p[1]))
        else:
            #Checar global
            dirVar, tipoVar = global_memoria.getDirMemory(str(p[1]))

        # quads.id_push(p[1], tipoVar) #Agregar id con varTipo
        # print(p[1])
        quads.id_push(dirVar, tipoVar) #Agregar dirs con varTipo

######################################################################################
#Estatutos

def p_llamada_fun(p):
    ''' llamada_fun : llamadaParam RP endParam SEMICOLON
                    | llamadaParam auxExp RP endParam SEMICOLON
                    | llamadaParam auxExp  RP endParam
    '''
    quads.operator_push('GoSub')
    #Obtener ID del procedimiento y su direccion en donde se encuentra
    quads.quadruples[quads.getID()].setResult(p[1])
    quadIni = superTabla.getQuadIni(p[1])
    quads.quadruples[quads.getID()].setLeftOp(quadIni)
    # Almacenar si es que regresa algo la funcion
    tipoRetorno = superTabla.getTipoRetornoFun(p[1])
    if(tipoRetorno != "void"):
        quads.setRetornoFuncion(p[1], tipoRetorno)

def p_llamadaParam(p):
    ''' llamadaParam : ID LP '''
    p[0] = p[1]
    # superTabla.set_currentTablaId(nameFunc)
    quads.operator_push('Era')
    #Buscar tamaño de la funcion llamada y hacer esto:
    quads.quadruples[quads.getID()].setResult(p[1])
    
def p_auxExp(p):
    ''' auxExp :  exp mandaParam
                | exp mandaParam COMMA auxExp
    '''

def p_mandaParam(p):
    ''' mandaParam : '''
    quads.operator_push('Param')

#Reinicar contador de parametros
def p_endParam(p):
    ''' endParam : '''
    quads.setContParam(0)

def p_retorno_fun(p):
    ''' retorno_fun :  RETURN LP exp finRetorno SEMICOLON
    '''
    currTabla = superTabla.get_currentTablaId()
    if(superTabla.getTipoRetornoFun(currTabla) == "void"):
        print("Error:", currTabla, " return cuando es funcion void.")
        sys.exit()


#Auxiliar para retorno
def p_finRetorno(p):
    ''' finRetorno : RP '''
    quads.operator_push("Return")

def p_lectura(p):
    ''' lectura : READ LP lecturaaux RP SEMICOLON'''

def p_lecturaaux(p):
    ''' lecturaaux : var lecturaSend
                    | var lecturaSend COMMA lecturaaux
    '''

def p_lecturaSend(p):
    ''' lecturaSend : '''
    quads.operator_push('Read')

def p_escritura(p):
    ''' escritura : PRINT LP escrituraAux RP SEMICOLON
    '''
    # quads.fillQuadruples() #fill quads (print -> asign)

def p_escrituraAux(p):
    ''' escrituraAux : exp escrituraEnd
                    | cartel escrituraEnd
                    | exp escrituraEnd COMMA escrituraAux
                    | cartel escrituraEnd COMMA escrituraAux
    '''
    #agregar el llamado funcion

def p_cartel(p):
    ''' cartel : STRING '''
    quads.string_push(p[1])

def p_escrituraEnd(p):
    ''' escrituraEnd : '''
    quads.operator_push('Print')


######################################################################################
#Condicionales

def p_decision(p):
    ''' decision : IF LP exp startIf THEN LCB estatutosAux endIf_Else
                | IF LP exp startIf THEN LCB estatutosAux startElse LCB estatutosAux endIf_Else
    '''

def p_startIf(p):
    ''' startIf : RP '''
    quads.operator_push('GoToF')
    quads.pilaSaltos.put(quads.getID())

def p_endIf_Else(p):
    ''' endIf_Else : RCB '''
    end = quads.pilaSaltos.get_nowait()
    nxtQuad = quads.getID()
    quads.quadruples[end].setResult(nxtQuad)

def p_startElse(p):
    ''' startElse : RCB ELSE '''
    quads.operator_push('GoTo')
    false = quads.pilaSaltos.get_nowait()
    quads.pilaSaltos.put(quads.getID())
    quads.quadruples[false].setResult(quads.getID())


def p_rep_condicional(p):
    ''' rep_condicional : MIENTRAS startWhile exp startWhile2 HACER LCB estatutosAux endWhile
    '''

def p_startWhile(p):
    ''' startWhile : LP '''
    quads.pilaSaltos.put(quads.getID()+1)

def p_startWhile2(p):
    ''' startWhile2 : RP '''
    quads.operator_push('GoToF')
    quads.pilaSaltos.put(quads.getID())

def p_endWhile(p):
    ''' endWhile : RCB '''
    end = quads.pilaSaltos.get_nowait()
    ret = quads.pilaSaltos.get_nowait()
    quads.operator_push('GoTo')
    quads.quadruples[quads.getID()].setResult(ret)
    quads.quadruples[end].setResult(quads.getID())

#For Loop
def p_rep_no_condicional(p):
    ''' rep_no_condicional : DESDE asign_vars HASTA rep_no_start exp rep_no_2 HACER asign_vars LCB  estatutosAux rep_no_end 
    '''

def p_rep_no_start(p):
    ''' rep_no_start : '''
    quads.pilaSaltos.put(quads.getID()+1)

def p_rep_no_2(p):
    ''' rep_no_2 : SEMICOLON  '''
    quads.operator_push('GoToF')
    quads.pilaSaltos.put(quads.getID())

def p_rep_no_end(p):
    ''' rep_no_end : RCB '''
    false = quads.pilaSaltos.get_nowait()
    ret = quads.pilaSaltos.get_nowait()
    quads.operator_push('GoTo')
    quads.quadruples[quads.getID()].setResult(ret)
    quads.quadruples[false].setResult(quads.getID())

### end For loop


def p_estatutosAux(p):
    ''' estatutosAux : estatutos estatutosAux
                        | estatutos 
    '''

def p_estatutos(p):
    ''' estatutos : asign_vars
                    | dec_vars
                    | llamada_fun
                    | lectura
                    | escritura
                    | decision
                    | rep_condicional
                    | retorno_fun
                    | rep_no_condicional
    '''

######################################################################################
#Expresiones

def p_exp(p):
    ''' exp : g_exp or g_exp
            | g_exp and g_exp
            | g_exp 
    '''

def p_or(p):
    ''' or : OR
    ''' 
    quads.operator_push("|")

def p_and(p):
    ''' and : AND
    '''
    quads.operator_push("&")

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
            | llamada_fun
    '''
    p[0] = p[1]


#Auxiliares identificadores expresion
def p_equalId(p):
    ''' equalId : EQUAL '''
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
    # quads.id_push(p[1], "entero") #Agregar a quads operations
    # print(p[1])
    quads.id_push(dirAux[0], "entero") #Agregar dir a quads operations

    
def p_ctef(p):
    ''' ctef : CTEF '''
    p[0] = p[1]
    ctes_memoria.setConstante(float(p[1])) #Agregar a memoria
    dirAux = ctes_memoria.getDirMemory(float(p[1]))
    # quads.id_push(p[1], "flotante") #Agregar a quads operations
    # print(p[1])
    quads.id_push(dirAux[0], "flotante") #Agregar dir a quads opeartions

def p_ctec(p):
    ''' ctec : CTEC '''
    p[0] = p[1]
    ctes_memoria.setConstante(str(p[1])) #Agregar a memoria
    dirAux = ctes_memoria.getDirMemory(str(p[1]))
    # quads.id_push(p[1], "char") #Agregar a quads operations
    quads.id_push(dirAux[0], "char") #Agrega dir a quads operations

######################################################################################
#Manejo errores
def p_error(p):
    token = f"{p.type}({p.value}) en linea {p.lineno}"
    print(f"Error de sintaxis: error {token}")
    sys.exit()

######################################################################################
#Crear ejecutable .obj
def crearOutFile():
    print("Generando archivo .obj ...")
    original_stdout = sys.stdout #Referencia original standar output
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    root = ROOT_DIR+"/Testing/objFiles/"
    nombreProg = superTabla.get_nombrePrograma() 
    with open(root+nombreProg+".obj", 'w') as f:
        sys.stdout = f #cambiar standar output to the file
        # print ctes in file
        print("### CTES ###")
        for key, value in ctes_memoria.getMemory().items():
            print(key,value)
        print("### dirFun ###")
        dirFunFormat() #Desplegar tabla de funciones
        #print quads in file
        print("### QUADS ###")
        listaQuads = quads.getListaQuads()
        for i in range(len(listaQuads)):
            #print con codigo de operacion
            print("%s %s %s %s" % (cod_operacion[listaQuads[i].getOperator()] ,listaQuads[i].getLeftOp(),listaQuads[i].getRightOp(), listaQuads[i].getResult()))
            # print("%s %s %s %s %s" % (listaQuads[i].getID(), listaQuads[i].getOperator(),listaQuads[i].getLeftOp(),listaQuads[i].getRightOp(), listaQuads[i].getResult()))
        #print 
        sys.stdout = original_stdout #resete standar output

#Darle formato a tabla de funciones
def dirFunFormat():
    dirAux = superTabla.dirFun.getDict()
    globalAux = dirAux["global"]
    dirAux.pop('global', None)
    #imprimir tabla global
    print("global",  "_".join(str(x) for x in globalAux["recursos"]["vars"]), "_".join(str(x) for x in globalAux["recursos"]["tmps"]), contObjetosFormat(globalAux["dicObjetos"]))
    #imprimir demas funciones/clases
    for key, val in dirAux.items():
        listParms = "_".join(val["listaParms"])
        if(not listParms): #if is empty
            listParms = None
        if(val['scope']!="global"):
            if(val['scope']=="class"): #clase
                print(val['scope'], key, "_".join(str(x) for x in val["recursos"]["vars"]), "_".join(str(x) for x in val["recursos"]["tmps"]), contObjetosFormat(val["dicObjetos"]))
            else:
                print(val['scope'], key, val['retorno'], val['quadIni'], listParms, "_".join((str(int) for int in val["recursos"]["vars"])), "_".join((str(int) for int in val["recursos"]["tmps"])), contObjetosFormat(val["dicObjetos"]))
        else:
            print(key, val["retorno"], val["quadIni"], listParms, "_".join((str(int) for int in val["recursos"]["vars"])), "_".join((str(int) for int in val["recursos"]["tmps"])), contObjetosFormat(val["dicObjetos"]))
    

#contador Objetos con formato para el .obj
def contObjetosFormat(dic):
    if(not dic):
        return None
    else:
        for key, value in dic.items():
            return str(key)+"_"+str(value)
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
# superTabla.printDirFun() #superTabla con funciones/clases/methodos
# superTabla.printTablaVars("global")
# superTabla.printTablaVars("pruebaUno")
# superTabla.printTablaVars("pruebaDos")
# superTabla.printTablaVars("precioConDescuento")
# superTabla.printTablaVars("Producto")
# superTabla.printListaParms("precioConDescuento")

