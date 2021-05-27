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

#######################################################   
#
stackParms = LifoQueue() #Maneja orden de parametros
stackExe = LifoQueue() #Maneja el orden de ejecucion
memoriaPrincipal = Memoria() #Maneja la memoria de ejecucion
quadruples = [] #Maneja cuadruplos
ip = 0 #Instruction Pointer

#######################################################   
#Operaciones del programa

#operaciones aritmeticas
def calcula(izq, op, der, dirRes):
    if(op == 1): # +
        memoriaPrincipal.setValMemory(dirRes, (izq + der))
    elif(op == 2): # -
        memoriaPrincipal.setValMemory(dirRes, (izq - der))
    elif(op == 3): # *
        memoriaPrincipal.setValMemory(dirRes, (izq * der))
    elif(op == 4): # /
        memoriaPrincipal.setValMemory(dirRes, (izq / der))
    elif(op == 5): # <
        memoriaPrincipal.setValMemory(dirRes, (izq < der))
    elif(op == 6): # >
        memoriaPrincipal.setValMemory(dirRes, (izq > der))
    elif(op == 7): # <=
        memoriaPrincipal.setValMemory(dirRes, (izq <= der))
    elif(op == 8): # >=
        memoriaPrincipal.setValMemory(dirRes, (izq >= der))
    elif(op == 9): # ==
        memoriaPrincipal.setValMemory(dirRes, (izq == der))
    elif(op == 10): # &
        memoriaPrincipal.setValMemory(dirRes, (izq and der))
    elif(op == 11): # |
        memoriaPrincipal.setValMemory(dirRes, (izq or der))

#######################################################   
#ejecutar programa
def ejecuta():

    codOp = 3
    # codOp = quadruples[ip] 
    # # while codOp != 17:
    if(codOp>=0 and codOp<=11): #operacion aritmetica
        izq = memoriaPrincipal.getValMemory(20500)
        der = memoriaPrincipal.getValMemory(20500)
        calcula(izq, codOp, der, 28000)
    elif(codOp == 12): # =
        pass
    elif(codOp == 13): # print
        pass
    elif(codOp == 14): # GoTo
        pass
    elif(codOp == 15): # GoToF
        pass
    elif(codOp == 16): # GoSub
        pass
    elif(codOp == 17): # endproc
        pass
    elif(codOp == 18): # return
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
        memoriaPrincipal.setValMemory(int(values[0]), values[1])
    #DirFunciones
    for index in range(startDirFun+1, startQuads):
        values = data[index].split()
    #QUADS
    for index in range(startQuads+1, len(data)):
        values = data[index].split()
        quadruples.append(values)
    
#Eliminar '/n' en el archivo.
def limpiarData(data):
    newData = []
    for i in range(len(data)):
        newData.append(data[i].rstrip('\n'))
    return newData

#######################################################   
# print para testing
def testing():
    print("###################################################################################")
    print("### Memoria Principal ###")
    memoriaPrincipal.printMemory()
    print("###################################################################################")
    print("### QUADS ###")
    for quad in quadruples:
        print(quad)
    print("###################################################################################")

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