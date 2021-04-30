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
        if(not self.pilaOperators.empty()): 
            pilaOperatorsTop = self.pilaOperators.get_nowait() #En caso de no estar vacio, que operador esta pila.
            self.pilaOperators.put(pilaOperatorsTop) #agregar de nuevo el operador a la pila

            if((pilaOperatorsTop == "+" or pilaOperatorsTop == "-") and (op == "*" or op == "/")):
                print("arreglar match en:", op)
                self.generateQuadruple(op)
                
            elif(op == "*" or op == "/"):
                print("arreglar match en:", pilaOperatorsTop)
                # self.generateQuadruple(op)
                self.operator_push(op)
            else:
                # print("agregar: ", op)
                self.pilaOperators.put(op)
        else:
            # print("agregar: ", op)
            self.pilaOperators.put(op)

    # ingresa a id.Name a la PilaO y id.Type a PilaT.
    def id_push(self, idName, idType):
        self.pilaOperands.put(idName)
        self.pilaTypes.put(idType)
    
    #genera cuadruplos de las listas mientras ya no haya valores a entrar.
    def fillQuadruples(self):
        while(not (self.pilaOperands.empty() or self.pilaOperators.empty())):
            self.generateQuadruple(self.pilaOperators.get_nowait())

    # genera el cuadruplo y lo guarda en la pila de quadruplos.
    def generateQuadruple(self, op):
        right_op = self.pilaOperands.get_nowait()
        right_type = self.pilaTypes.get_nowait()
        left_op = self.pilaOperands.get_nowait()
        left_type = self.pilaTypes.get_nowait()
        operator = op
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
    qm.id_push("A", "entero")
    qm.operator_push("+")
    qm.id_push("B", "entero")
    qm.operator_push("*")
    qm.id_push("C", "entero")

    # qm.operator_push("+")
    # qm.id_push("D", "entero")
    # qm.operator_push("*")
    # qm.id_push("E", "entero")
    # qm.operator_push("*")
    # qm.id_push("F", "entero")


    qm.fillQuadruples()
    qm.print_stacks()
    qm.print_quadruples()

main()



    
