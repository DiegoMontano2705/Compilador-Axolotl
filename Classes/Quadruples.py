# 
#     Clase Quadruples: estructura de datos para generacion de quadruples.  .
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez 
# 

class Quadruples:
    
    def __init__(self,id,operator,leftOp, rightOp, result):
        self.id = id
        self.leftOp = leftOp
        self.rightOp = rightOp
        self.operator = operator
        self.result = result
    
    def printQuad(self):
        print(self.id,self.operator, self.leftOp, self.rightOp, self.result)
    
    def getLeftOp(self):
        return self.leftOp
    
    def getRightOp(self):
        return self.rightOp

    def setID(self,id):
        self.id = id
    
    def getID(self):
        return self.id

    def getResult(self):
        return self.result

    def setResult(self,result):
        self.result = result
    
    def getOperator(self):
        return self.operator
    
    def setOperator(self,operator):
        self.operator = operator
