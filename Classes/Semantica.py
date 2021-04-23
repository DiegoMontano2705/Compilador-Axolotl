# 
#     Clase Semantica: estructura de datos para validacion y consulta de tipos de retorno operaciones.
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez 
# 

class Semantica:

    #Entero,+,-: 0
    # Float,*,/: 1
    # Char,>,<,<=,>=: 2
    # Bool, =: 3
    # &, | : 4
    # Err = -1
    #[leftOperando][righOperando][operador]
    def __init__(self):       
        self.cuboSemantico = (
                                (   #+ * > = &
                                    (0,1,3,0, -1), #entero entero
                                    (-1,-1,-1,-1,-1), #entero float
                                    (-1,-1,-1,-1,-1), #entero char
                                    (-1,-1,-1,-1,-1), #entero bool
                                ),
                                (
                                    (-1,-1,-1,-1,-1), #float entero
                                    (1,1,3,1,-1), #float float
                                    (-1,-1,-1,-1,-1), #float char
                                    (-1,-1,-1,-1,-1), #float bool
                                ),
                                (
                                    (-1,-1,-1,-1,-1), #char entero
                                    (-1,-1,-1,-1,-1), #char float
                                    (-1,-1,-1,2,-1), #char char
                                    (-1,-1,-1,-1,-1), #char bool
                                ),
                                (
                                    (-1,-1,-1,-1,-1), #Bool entero
                                    (-1,-1,-1,-1,-1), #Bool float
                                    (-1,-1,-1,-1,-1), #Bool char
                                    (-1,-1,3,3,3), #Bool bool
                                ),
                             )
    
    #Convierte el indice del cubo al tipo necesario. 
    def equivalentReturn(self, stm):
        if(stm==0):
            return "entero"
        elif(stm==1):
            return "float"
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
        elif(stm=="float" or stm=="*" or stm=="/"): # Float,*,/: 1
            return 1
        elif(stm=="bool" or stm=="="): # Bool, =: 3
            return 3
        elif(stm=="char" or stm==">" or stm=="<", stm=="<=" or stm==">=" or stm=="&" or stm=="|"): # Char,>,<,<=,>=, &, |: 2
            return 2
        elif(stm=="&" or stm=="|"): # &, |: 4
            return 4        
        else:
            print("Error: Atributos no disponibles en cubo semantico.")        

    #Regresa el tipo del resultado entre leftOp op rightOp
    def resTipo(self,leftOp, rightOp, op):
        leftOp = self.equivalent(leftOp)
        rightOp = self.equivalent(rightOp)
        op = self.equivalent(op)
        return self.equivalentReturn(self.cuboSemantico[leftOp][rightOp][op])

def main():
    sem = Semantica()
    print(sem.resTipo("entero","entero","="))
    print(sem.resTipo("float","float","="))
    print(sem.resTipo("float","float","+"))
    print(sem.resTipo("bool","bool","&"))
    print(sem.resTipo("entero","float","="))


main()

    