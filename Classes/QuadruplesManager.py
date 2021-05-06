# 
#     Clase Quadruples: estructura de datos para generacion de quadruples.  .
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez 
# 
from queue import LifoQueue
import queue
from Quadruples import *
from Semantica import *
from Temporal import *

opUntil = ['>', '<', '>=', '<=']

class QuadruplesManager:

    def __init__(self):
        self.idNum = -1   # numero de quadruplo, sirve sobre todo para Conditions y Loops
        self.pilaOperands = LifoQueue() #stack que almacena los operandos.
        self.pilaTypes = LifoQueue() #stack que almacena los tipos de los operandos.
        self.pilaOperators = LifoQueue() #stack que almacena operadores.
        self.quadruples = queue.Queue() #queue que almacena los quadruples generados.
        self.semantica = Semantica() #genera cubo semántico para validación de tipos.
        self.tmp = Temporal() #objeto de la clase Temporal, administra los temporales y la memoria.
        self.pilaSaltos = LifoQueue() #pila que almacena los saltos pendientes
    
    def getID(self):
        return self.idNum

    def setID(self,idNum):
        self.idNum = idNum

    #Inspeccionar si ya se tiene almacenado un tipo similar.
    def operator_push(self,op):
        #Caso de encontrarse + o - ya habiendo un + o - en la pila.
        # if(self.pilaOperators.qsize()>0):
        #     pilaOperatorsTop = self.pilaOperators.get_nowait() #Que operador esta top stack.
        #     self.pilaOperators.put(pilaOperatorsTop) #agregar de nuevo el operador a la stack
        #     if((op == "+" or op == "-") and (pilaOperatorsTop== "+" or pilaOperatorsTop == "-")):
        #         self.generateQuadruple()
        #         self.pilaOperators.put(op)
        
        if(op == '('):
            self.solveQuadruplesUntil(op)
        elif(op in opUntil):
            self.fillQuadruples()
            self.pilaOperators.put(op)
        else:
            self.pilaOperators.put(op)
            

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
                    self.generateQuadruple()
                elif(self.pilaOperators.qsize()>1):
                    pilaOperatorsTop = self.pilaOperators.get_nowait() #Que operador esta top stack.
                    pilaOperators2 = self.pilaOperators.get_nowait() #Que operador esta 2do top stack.
                    self.pilaOperators.put(pilaOperators2) #agregar de nuevo el operador a la stack
                    self.pilaOperators.put(pilaOperatorsTop) #agregar de nuevo el operador a la stack
                    if((pilaOperatorsTop == "+" or pilaOperatorsTop == "-") and (pilaOperators2 == "+" or pilaOperators2 == "-")):
                        self.pilaOperands.get_nowait()     
                        self.pilaTypes.get_nowait() 
                        self.pilaOperators.get_nowait()
                        self.generateQuadruple()
                        self.pilaOperands.put(idName)
                        self.pilaTypes.put(idType)
                        self.pilaOperators.put(pilaOperatorsTop)


    #Genera cuadruplos cuando se encuentra ), hasta volver a encontra (.
    def solveQuadruplesUntil(self, op):
        while(not op == "("):
            self.generateQuadruple()
            op = self.pilaOperators.get_nowait()

    #genera cuadruplos de las listas mientras ya no haya valores a entrar.
    def fillQuadruples(self):
        while(not self.pilaOperators.empty()):
            self.generateQuadruple()

    # genera el cuadruplo y lo guarda en la pila de quadruplos.
    def generateQuadruple(self):
        operator = self.pilaOperators.get_nowait()
        if(not (operator=="(" or operator==")")):
            if (operator == "GoTo"):
                left_op = self.pilaOperands.get_nowait()
                operator = "GoToF"   #Se cambia la el operador a su contrario debido al manejor de Pilas que lee las operaciones al reves
                if(left_op != None): #and self.pilaTypes.get_nowait() == 'bool'):
                    id_Final = (self.getID() + 1)
                    q = Quadruples(id_Final,operator, left_op, None, None)
                    self.setID(self.getID() + 1)
                    self.pilaSaltos.put(self.getID()) #Guardas id del if en pila de saltos
                    self.quadruples.put(q)

            elif(operator == "GoToF"):
                operator = "GoTo"   #Se cambia la el operador a su contrario debido al manejor de Pilas que lee las operaciones al reves
                saltoFalso = self.pilaSaltos.get_nowait() #Obtener id del salto del if anterior
                id_Final = (self.getID() + 1)
                q = Quadruples(id_Final,operator,None, None,saltoFalso)
                self.setID(self.getID() + 1)
                self.pilaSaltos.put(self.getID()) #Guardas id del else en pila de saltos
                self.quadruples.put(q)
            else :    
                right_op = self.pilaOperands.get_nowait()
                right_type = self.pilaTypes.get_nowait()
                left_op = self.pilaOperands.get_nowait()
                left_type = self.pilaTypes.get_nowait()
                # print("my operator", operator)
                result_type = self.semantica.resTipo(operator, left_type, right_type) #Es posible la operacion? y que retorna?
                if(result_type != None):    
                    result = self.tmp.next() #preparar temporal
                    id_Final = (self.getID() + 1)
                    q = Quadruples(id_Final,operator, left_op, right_op, result)
                    self.setID(self.getID() + 1)
                    self.quadruples.put(q)
                    self.pilaOperands.put(result)
                    self.pilaTypes.put(result_type)

    #Poner salto de if cuando se termina el condicional       
    def endCondStatment(self):
        end = self.pilaSaltos.get_nowait()
        # Rellenar GoToF con el end -> ver este problema pues no se tienen metodo para acceder a index del Queue de Quedruples


    def print_stack(self):
        print("pilaOperands: ")
        while not self.pilaOperands.empty():
            print(self.pilaOperands.get(), end=" ")
        print('\n')
        print("pilaOperators: ")
        while not self.pilaOperators.empty():
            print(self.pilaOperators.get(), end=" ")
        print('\n')   

    def print_quadruples(self):
        while not self.quadruples.empty():
            self.quadruples.get().printQuad()
 

def main():
    qm = QuadruplesManager()
    #A - ( B + C) * D * E ->
    #+ B C t0
    #* t0 D t1
    #* t1 E t2
    #- A t2 t3

    # if(A + B > C){  # GOTOF t3 8
    #   C * D
    # }
    # else {
    # C + D
    # }
    
    #Test Conditional
    # qm.id_push("A", "float")
    # qm.operator_push("+")
    # qm.id_push("B", "float")
    # qm.operator_push("*")
    # qm.id_push("D", "float")
    # ##First If
    # qm.operator_push("GoToF")
    # qm.id_push("A", "float")
    # qm.operator_push("+")
    # qm.id_push("B", "float")
    # ## Else
    # qm.operator_push("GoTo")
    # qm.id_push("C", "float")
    # qm.operator_push("-")
    # qm.id_push("D", "float")
    # qm.fillQuadruples()
    # qm.print_quadruples()



    #Test operations
    qm.id_push("A", "float")
    qm.operator_push(">")
    qm.id_push("B", "float")
    qm.operator_push("+")
    qm.id_push("C", "float")
    qm.fillQuadruples()
    qm.print_quadruples()
    
main()



    
