# 
#     Clase Quadruples: estructura de datos para generacion de quadruples.  .
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez 
# 

class Quadruples:
    
    def __init__(self,operator,leftOp, rightOp, result):
        self.leftOp = leftOp
        self.rightOp = rightOp
        self.operator = operator
        self.result = result
    
    def printQuad(self):
        print(self.operator, self.leftOp, self.rightOp, self.result)