# 
#     Clase Semantica: estructura de datos para validacion y consulta de tipos de retorno operaciones.
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez 
# 
import sys
class Semantica:

    #Entero,+,-: 0
    # flotante, /: 1
    # Char,>,<,<=,>=: 2
    # Bool, =: 3
    # &, | : 4
    # * : 5
    # ==, != : 6
    # Err = -1
    #[leftOperando][righOperando][operador]
    def __init__(self):       
        self.cuboSemantico = (
                                (   #+ / > = & * ==
                                    (0,1,3,0, -1, 0, 3), #entero entero
                                    (-1,-1,-1,-1,-1,-1, -1), #entero flotante
                                    (-1,-1,-1,-1,-1,-1, -1), #entero char
                                    (-1,-1,-1,-1,-1,-1, -1), #entero bool
                                ),
                                (
                                    (-1,-1,-1,-1,-1,-1, -1), #flotante entero
                                    (1, 1, 3, 1, -1, 1, 3), #flotante flotante
                                    (-1,-1,-1,-1,-1,-1, -1), #flotante char
                                    (-1,-1,-1,-1,-1,-1, -1), #flotante bool
                                ),
                                (
                                    (-1,-1,-1,-1,-1,-1, -1), #char entero
                                    (-1,-1,-1,-1,-1,-1, -1), #char flotante
                                    (-1,-1,-1,2,-1,-1, 3), #char char
                                    (-1,-1,-1,-1,-1,-1, -1), #char bool
                                ),
                                (
                                    (-1,-1,-1,-1,-1,-1, -1), #Bool entero
                                    (-1,-1,-1,-1,-1,-1, -1), #Bool flotante
                                    (-1,-1,-1,-1,-1,-1, -1), #Bool char
                                    (-1,-1,3,3,3,-1, 3), #Bool bool
                                ),
                             )
    
    #Convierte el indice del cubo al tipo necesario. 
    def equivalentReturn(self, stm):
        if(stm==0):
            return "entero"
        elif(stm==1):
            return "flotante"
        elif(stm==2):
            return "char"
        elif(stm==3):
            return "bool"
        elif(stm==-1):
            print("Error: La operacion con esos tipos no es compatible.")  

    #Convierte el input a indice para el cubo
    def equivalent(self, stm):
        if(stm=="entero" or stm=="+" or stm=="-"): #Entero,+,-: 0
            return 0
        elif(stm=="*"): # * : 5
            return 5  
        elif(stm=="flotante" or stm=="/"): # flotante,*,/: 1
            return 1
        elif(stm=="bool" or stm=="="): # Bool, =: 3
            return 3
        elif(stm=="char" or stm==">" or stm=="<", stm=="<=" or stm==">=" or stm=="&" or stm=="|"): # Char,>,<,<=,>=, &, |: 2
            return 2
        elif(stm=="&" or stm=="|"): # &, |: 4
            return 4 
        elif(stm=="==" or stm=="!="):
            return 6     
        else:
            return -1      

    #Regresa el tipo del resultado entre leftOp op rightOp
    def resTipo(self,op, leftOp, rightOp):
        leftOpCode = self.equivalent(leftOp)
        rightOpCode = self.equivalent(rightOp)
        opCode = self.equivalent(op)
        res = self.cuboSemantico[leftOpCode][rightOpCode][opCode]

        if(res >= 0):
            return self.equivalentReturn(res)
        else:
            print("Error: operacion entre", leftOp, op, rightOp, "no es posible")
            sys.exit()

# def main():
#     sem = Semantica()
#     print(sem.resTipo("*", "flotante","flotante"))
#     # print(sem.resTipo("=","flotante","flotante"))
#     # print(sem.resTipo("+","flotante","flotante"))
#     # print(sem.resTipo("&","bool","bool"))
#     # print(sem.resTipo("=","entero","flotante"))
 

# main()

    