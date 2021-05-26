# 
#     Clase MaquinaVirtual: Ejecuta el archivo obj.
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez 
# 
#######################################################   
import sys
from Classes.Memoria import *
from queue import LifoQueue


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
#######################################################   
#
stackExe = LifoQueue() #Maneja el orden de ejecucion
memoriaPrincipal = Memoria() #Maneja la memoria de ejecucion
IP = 1 #Instruction Pointer

#######################################################   
#ejecutar programa
def ejecuta():
    pass
#######################################################   
#ejecutar programa
def prepararData():
    
    pass
#######################################################   
# print para testing
def log():
    pass
#######################################################   
if __name__ == '__main__':
    if (len(sys.argv)>1):
        file = sys.argv[1]
        try:
            f = open("/Testing/"+file, 'r')
            data = f.readlines()
            f.close()
            prepararData(data)
            ejecuta()
            log()
        except EOFError:
            print(EOFError)
    else:
        print(sys.argv[1], ".obj no existente.")