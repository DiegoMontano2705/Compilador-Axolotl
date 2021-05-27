# 
#     Clase MaquinaVirtual: Ejecuta el archivo obj.
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez 
# 
#######################################################   
import sys
import os
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
stackParms = LifoQueue() #Maneja orden de parametros
stackExe = LifoQueue() #Maneja el orden de ejecucion
memoriaPrincipal = Memoria() #Maneja la memoria de ejecucion
IP = 1 #Instruction Pointer

#######################################################   
#ejecutar programa
def ejecuta():
    pass


#######################################################   
#prepararDatos
def prepararData(data):
    data = limpiarData(data)
    #Constantes
    startCtes = data.index("### CTES ###")
    startDirFun = data.index("### dirFun ###")
    startQuads = data.index("### QUADS ###")
    for index in range(startCtes+1, startDirFun):
        values = data[index].split()
        memoriaPrincipal.setValMemory(values[0], values[1])
    #DirFunciones
    for index in range(startDirFun+1, startQuads):
        values = data[index].split()
        print(values)
        pass
    #QUADS
    print("#quads")
    for index in range(startQuads+1, len(data)):
        values = data[index].split()
        print(values)
    
    pass

#Eliminar '/n'
def limpiarData(data):
    newData = []
    for i in range(len(data)):
        newData.append(data[i].rstrip('\n'))
    return newData
#######################################################   
# print para testing
def testing():
    memoriaPrincipal.printMemory()
    pass
#######################################################   
if __name__ == '__main__':
    if (len(sys.argv)>1):
        file = sys.argv[1]
        try:
            ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
            f = open(ROOT_DIR+"/Testing/objFiles/"+file, 'r')
            data = f.readlines()
            f.close()
            print("Ejecutando", file, "...")
            prepararData(data)
            ejecuta()
            testing()
        except EOFError:
            print(EOFError)
    else:
        print(sys.argv[1], ".obj no existente.")