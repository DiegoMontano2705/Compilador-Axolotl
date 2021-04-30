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

class QuadruplesManager:

    def __init__(self):
        self.pilaOperands = LifoQueue() #pila que almacena los operandos.
        self.pilaTypes = LifoQueue() #pila que almacena los tipos de los operandos.
        self.pilaOperators = LifoQueue()
        self.quadruples = queue.Queue() #pila que almacena los quadruples generados.
        self.semantica = Semantica() #genera cubo semántico para validación de tipos.
        self.tmp = Temporal() #objeto de la clase Temporal, administra los temporales y la memoria.
    
    #Inspeccionar si ya se tiene almacenado un tipo similar.
    def operator_push(self, op):
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

            if(pilaOperatorsTop == "*" or pilaOperatorsTop == "/"):
                self.generateQuadruple()
            elif(self.pilaOperators.qsize()>1):
                pilaOperatorsTop = self.pilaOperators.get_nowait() #Que operador esta top stack.
                pilaOperators2 = self.pilaOperators.get_nowait() #Que operador esta 2do top stack.
                self.pilaOperators.put(pilaOperatorsTop) #agregar de nuevo el operador a la stack
                self.pilaOperators.put(pilaOperators2) #agregar de nuevo el operador a la stack
                
                if((pilaOperatorsTop == "+" or pilaOperatorsTop == "-") and (pilaOperators2 == "+" or pilaOperators2 == "-")):
                    self.pilaOperands.get_nowait()     
                    self.pilaTypes.get_nowait()        
                    self.generateQuadruple()
                    self.pilaOperands.put(idName)
                    self.pilaTypes.put(idType)
        
    
    #genera cuadruplos de las listas mientras ya no haya valores a entrar.
    def fillQuadruples(self):
        while(not self.pilaOperators.empty()):
            self.generateQuadruple()

    # genera el cuadruplo y lo guarda en la pila de quadruplos.
    def generateQuadruple(self):
        right_op = self.pilaOperands.get_nowait()
        right_type = self.pilaTypes.get_nowait()
        left_op = self.pilaOperands.get_nowait()
        left_type = self.pilaTypes.get_nowait()
        operator = self.pilaOperators.get_nowait()
        result_type = self.semantica.resTipo(operator, left_type, right_type) #Es posible la operacion? y que retorna?
        if(result_type != None):    
            result = self.tmp.next() #preparar temporal
            q = Quadruples(operator, left_op, right_op, result)
            self.quadruples.put(q)
            self.pilaOperands.put(result)
            self.pilaTypes.put(result_type)

    
    def print_stacks(self):
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
    #A * B / C + D * E ->
    #* A B t1
    #/ t1 C t2
    #* D E t3
    #+ t2 t3 t4
    qm.id_push("A", "float")
    qm.operator_push("*")
    qm.id_push("B", "float")
    qm.operator_push("/")
    qm.id_push("C", "float")
    qm.operator_push("+")
    qm.id_push("D", "float")
    qm.operator_push("*")
    qm.id_push("E", "float")
    qm.fillQuadruples()
    qm.print_quadruples()

main()



    
