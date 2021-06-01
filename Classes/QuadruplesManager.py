#
#     Clase Quadruples: estructura de datos para generacion de quadruples.  .
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez
#
from queue import LifoQueue
import sys
import queue

from Classes.Quadruples import *
from Classes.Semantica import *
from Classes.Temporal import *
# from Quadruples import *
# from Semantica import *
# from Temporal import *


opUntil = ['>', '<', '>=', '<=', '=', '|', '&']
opCond_Loops = ['GoToF', 'GoTo', 'GoToV']
opModules = ['EndFunc','Return']
opCallFunc = ['GoSub', 'Era', 'Param']

class QuadruplesManager:

    def __init__(self):
        self.idNum = -1   # numero de quadruplo
        self.pilaOperands = LifoQueue() #stack que almacena los operandos.
        self.pilaTypes = LifoQueue() #stack que almacena los tipos de los operandos.
        self.pilaOperators = LifoQueue() #stack que almacena operadores.
        self.quadruples = [] #lista que almacena los quadruples generados.
        self.semantica = Semantica() #genera cubo semántico para validación de tipos.
        self.tmp = Temporal() #objeto de la clase Temporal, administra los temporales y la memoria.
        self.pilaSaltos = LifoQueue() #pila que almacena los saltos pendientes
        self.contParams = 0         #contador para saber que parametro esta recibiendo cuando se llama una funcion/modulo
        self.currTabla = "global" #Saber en que contexto se encuentra para el manejo de temporales.
######################################################################################
#set and gets

    def getID(self):
        return self.idNum

    def setID(self,idNum):
        self.idNum = idNum

    def getContParam(self):
        return self.contParams

    def getListaQuads(self):
        return self.quadruples

    #Regresa recursos temporales utilizados localmente
    def getRecursosTmpsLocales(self):
        return self.tmp.getListaTemporalesLocales()

    #Regresa recursos temporales utilizados globalmente
    def getRecursosTmpsGlobales(self):
        return self.tmp.getListaTemporalesGlobales()

    #Se usa para reinicar el contador a cero despues de que llamas todos los parametros de una funcion/modulo
    def setContParam(self,contParams):
        self.contParams = contParams

    #set curr Tabla para direccion temporales
    def setCurrTabla(self, cTabla):
        self.currTabla = cTabla

    #Reset a contador de tmps
    def clearTmps(self):
        self.tmp.clear()

    #set endprog
    def setEndProg(self):
        self.quadruples
        q = Quadruples(None,"endprog",None,None,None)
        self.quadruples.append(q)

    #set return Quad
    def setRetornoFuncion(self, nomFun, tipoRetorno):
        result = self.tmp.next(tipoRetorno, self.currTabla) #preparar temporal
        val = self.tmp.next(tipoRetorno, self.currTabla) #temporal con el valor.
        q = Quadruples(None,'=',val,None,result)
        self.setID(self.getID()+1)
        self.quadruples.append(q)
        self.pilaOperands.put(result)
        self.pilaTypes.put(tipoRetorno)

    #set Era
    def setEra(self, nomFun):
        self.quadruples
        q = Quadruples(None,'Era',nomFun,None, None)
        self.setID(self.getID()+1)
        self.quadruples.append(q)


######################################################################################
#operator push

    #Inspeccionar si ya se tiene almacenado un tipo similar.
    def operator_push(self,op):
        if(op == ')'):
            self.solveQuadruplesUntil(op)
        elif(op in opUntil):
            self.fillQuadruples()
            self.pilaOperators.put(op)
        elif( (op in opCond_Loops) or (op in opModules) or  op == 'Print' or op == 'Read'):
            self.fillQuadruples()
            self.generateQuadruple(op)
        elif(op in opCallFunc):
            self.generateQuadruple(op)
        else:
            self.pilaOperators.put(op)

######################################################################################
# id push
    # ingresa a id.Name a la PilaO y id.Type a PilaT.
    def id_push(self, idName, idType):
        #push id & type
        self.pilaOperands.put(idName)
        self.pilaTypes.put(idType)

        if(not self.pilaOperators.empty()):
            #check pasados operators
            pilaOperatorsTop = self.pilaOperators.get_nowait() #Que operador esta top stack.
            self.pilaOperators.put(pilaOperatorsTop) #agregar de nuevo el operador a la stack
            if(not pilaOperatorsTop == "("): #Fondo falso / salta
                if(pilaOperatorsTop == "*" or pilaOperatorsTop == "/"):
                    operator = self.pilaOperators.get_nowait()
                    self.generateQuadruple(operator)
                elif(self.pilaOperators.qsize()>1):
                    pilaOperatorsTop = self.pilaOperators.get_nowait() #Que operador esta top stack.
                    pilaOperators2 = self.pilaOperators.get_nowait() #Que operador esta 2do top stack.
                    self.pilaOperators.put(pilaOperators2) #agregar de nuevo el operador a la stack
                    self.pilaOperators.put(pilaOperatorsTop) #agregar de nuevo el operador a la stack
                    if((pilaOperatorsTop == "+" or pilaOperatorsTop == "-") and (pilaOperators2 == "+" or pilaOperators2 == "-")):
                        self.pilaOperands.get_nowait()
                        self.pilaTypes.get_nowait()
                        self.pilaOperators.get_nowait()
                        operator = self.pilaOperators.get_nowait()
                        self.generateQuadruple(operator)
                        self.pilaOperands.put(idName)
                        self.pilaTypes.put(idType)
                        self.pilaOperators.put(pilaOperatorsTop)

    #Solo se usara en print(escribe)
    def string_push(self, strAux):
        strAux = strAux.replace(" ", "_") #solve problem with spaces
        self.pilaOperands.put(strAux[1:-1]) #without " "


######################################################################################
#Quads helpers

    #Genera cuadruplos cuando se encuentra ), hasta volver a encontra (.
    def solveQuadruplesUntil(self, op):
        while(not op == "("):
            operator = self.pilaOperators.get_nowait()
            self.generateQuadruple(operator)
            op = self.pilaOperators.get_nowait()

    #Genera cuadruplos hasta que se encuentra =, sirve para resolver parametros.
    def solveQuadruplesParms(self, op):
        while(not op == "="):
            self.generateQuadruple(op)
            op = self.pilaOperators.get_nowait()

    #genera cuadruplos de las listas mientras ya no haya valores a entrar.
    def fillQuadruples(self):
        while(not self.pilaOperators.empty()):
            operator = self.pilaOperators.get_nowait()
            self.generateQuadruple(operator)

    # genera el cuadruplo y lo guarda en la pila de quadruplos.
    def generateQuadruple(self,operator):
        if(not (operator=="(" or operator==")")):
            ## No-Lineales
            if (operator == "GoToF"):
                left_op = self.pilaOperands.get_nowait()
                if(left_op != None and self.pilaTypes.get_nowait() == 'bool'):
                    id_Final = (self.getID() + 1)
                    q = Quadruples(id_Final,operator, left_op, None, None)
                    self.setID(self.getID() + 1)
                    #self.pilaSaltos.put(self.getID()) #Guardas id del if en pila de saltos
                    self.quadruples.append(q)
                else:
                    raise Exception("Error Type-mismatch: Valor no es booleano")
                    #print("Error Type-mismatch: Value not boolean :",left_op )
                    #sys.exit()

            elif(operator == "GoTo" or operator == 'GoToV'):
                id_Final = (self.getID() + 1)
                q = Quadruples(id_Final,operator,None, None,None)
                self.setID(self.getID() + 1)
                #self.pilaSaltos.put(self.getID()) #Guardas id del else en pila de saltos
                self.quadruples.append(q)

            ## print, write y return
            elif(operator == 'Print' or operator == 'Return' or operator == 'Read'):
                left_op = left_op = self.pilaOperands.get_nowait()
                if(left_op != None ):
                    id_Final = (self.getID() + 1)
                    q = Quadruples(id_Final,operator,None, None,left_op)
                    self.setID(self.getID() + 1)
                    self.quadruples.append(q)
            #elif(operator == 'read'):


            ## Modulos
            elif(operator == 'EndFunc' or operator == 'Era' or operator == 'GoSub'):
                id_Final = (self.getID() + 1)
                q = Quadruples(id_Final,operator,None, None,None)
                self.setID(self.getID() + 1)
                self.quadruples.append(q)

            elif(operator == 'Param'):
                
                #Si hay cosas que resolver en parametros, resuelve hasta el =.
                if(self.pilaOperators.qsize() >1): 
                    self.solveQuadruplesParms(self.pilaOperators.get_nowait())

                left_op = self.pilaOperands.get_nowait()
                if(left_op != None):
                    id_Final = (self.getID() + 1)
                    self.setContParam(self.getContParam()+1)
                    q = Quadruples(id_Final,operator,left_op, None,self.getContParam())
                    self.setID(self.getID() + 1)
                    self.quadruples.append(q)

            #####
            else:
                right_op = self.pilaOperands.get_nowait()
                right_type = self.pilaTypes.get_nowait()
                left_op = self.pilaOperands.get_nowait()
                left_type = self.pilaTypes.get_nowait()
                # print("my operator", operator)
                result_type = self.semantica.resTipo(operator, left_type, right_type) #Es posible la operacion? y que retorna?
                if(result_type != None):
                    id_Final = (self.getID() + 1)
                    if(operator == '='):
                        q = Quadruples(id_Final,operator, right_op, None,left_op )
                        self.setID(self.getID() + 1)
                        self.quadruples.append(q)
                    else:
                        result = self.tmp.next(result_type, self.currTabla) #preparar temporal
                        q = Quadruples(id_Final,operator, left_op, right_op, result)
                        self.setID(self.getID() + 1)
                        self.quadruples.append(q)
                        self.pilaOperands.put(result)
                        self.pilaTypes.put(result_type)

######################################################################################
# Testing
    def print_stack(self):
        print("pilaOperands: ")
        while not self.pilaOperands.empty():
            print(self.pilaOperands.get(), end=" ")
        print('\n')
        print("pilaOperators: ")
        while not self.pilaOperators.empty():
            print(self.pilaOperators.get(), end=" ")
        print('\n')

    #print for testing
    def print_quadruples(self):
        myfile = open('quads.txt', 'w')
        for i in range(len(self.quadruples)):
            #quad = self.quadruples[i].printQuad()
            # myfile.write("%s \n" % self.quadruples[i].printQuad())
            myfile.write("%s %s %s %s %s \n" % (self.quadruples[i].getID(), self.quadruples[i].getOperator() ,self.quadruples[i].getLeftOp(),self.quadruples[i].getRightOp(), self.quadruples[i].getResult()))
        myfile.close()


# if __name__ == '__main__':
#    qm = QuadruplesManager()
#    qm.id_push("A", "float")
#    qm.operator_push("*")
#    qm.operator_push("(")
#    qm.id_push("B", "float")
#    qm.operator_push("+")
#    qm.id_push("C", "float")
#    qm.operator_push(")")
#    # qm.print_stacks()
#    qm.fillQuadruples()
#    qm.print_quadruples()

#     # if(A + B > C){  # GOTOF t3 8
#     #   C * D
#     # }
#     # else {
#     # C + D
#     # }

#     # #Test Conditional
#     # qm.id_push("A", "float")
#     # qm.operator_push("*")                    #Op GOTOF
#     # qm.id_push("B", "float")                 #id
#     # ##First If                              QUAD * A B T0
#     # qm.operator_push("GoToF")
#     # qm.id_push("C", "float")
#     # qm.operator_push("+")
#     # qm.id_push("D", "float")
#     # # Else
#     # qm.operator_push("GoTo")
#     # qm.id_push("E", "float")
#     # qm.operator_push("-")
#     # qm.id_push("F", "float")
#     # qm.fillQuadruples()
#     # qm.print_stack()
#     # qm.print_quadruples()

#     #Test Conditional
# #    qm.operator_push('(')
# #    qm.id_push("A", "float")
# #    qm.operator_push(">")
# #    qm.id_push("B", "float")
# #    qm.operator_push("-")
# #    qm.id_push("D", "float")
# #    qm.operator_push(')')
#     ##First If
# #    qm.operator_push('GoToF')
# #    qm.id_push("F", "float")
# #    qm.operator_push("+")
# #    qm.id_push("G", "float")
#     ## Else
# #    qm.operator_push('GoTo')
# #    qm.id_push("H", "float")
# #    qm.operator_push("*")
# #    qm.id_push("I", "float")



# #     #Test operations
# #    qm.id_push("A", "float")
# #    qm.operator_push("=")
# #    qm.id_push("B", "float")
# #    qm.operator_push("*")
# #    qm.id_push("C", "float")
# #    qm.operator_push("+")
# #    qm.id_push("D", "float")
# #    qm.operator_push("-")
# #    qm.id_push("E", "float")
# #    qm.fillQuadruples()
# #    qm.print_quadruples()

#      #Test print
#     # qm.id_push("A", "float")
#     # qm.operator_push("=")
#     # qm.id_push("B", "float")
#     # qm.operator_push("*")
#     # qm.id_push("C", "float")
#     # qm.operator_push("+")
#     # qm.id_push("D", "float")
#     # qm.operator_push("-")
#     # qm.id_push("E", "float")
#     # qm.operator_push('print')

#     #Test constantes
#    qm.id_push("a", "entero")
#    qm.operator_push("=")
#    qm.id_push("4", "entero")
#    qm.fillQuadruples()
#    qm.id_push("b", "entero")
#    qm.operator_push("=")
#    qm.id_push("5", "entero")
#    qm.operator_push("+")
#    qm.id_push("5", "entero")
#    qm.operator_push("+")
#    qm.id_push("4", "entero")
#    qm.operator_push("-")
#    qm.id_push("2", "entero")
#    qm.fillQuadruples()
#    qm.print_quadruples()





