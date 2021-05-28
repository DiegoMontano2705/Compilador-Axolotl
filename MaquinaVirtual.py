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
    ip = 0 #Instruction Pointer
    codOp = int(quadruples[ip][0])

    #Mientras no encuentre fin del programa.
    while codOp != 17:
        codOp = int(quadruples[ip][0]) #Codigo de operacion
        if(codOp>=0 and codOp<=11): #operacion aritmetica
            izq = memoriaPrincipal.getValMemory(int(quadruples[ip][1]))
            der = memoriaPrincipal.getValMemory(int(quadruples[ip][2]))
            res = int(quadruples[ip][3])
            calcula(izq, codOp, der, res)
        elif(codOp == 12): # =
            val = memoriaPrincipal.getValMemory(int(quadruples[ip][1]))
            res = int(quadruples[ip][3])
            memoriaPrincipal.setValMemory(res, val)
        elif(codOp == 13): # print
            try: #if not work with value, so its a string
                val = memoriaPrincipal.getValMemory(int(quadruples[ip][3]))
            except: #work with strings
                strAux = str(quadruples[ip][3:][0])
                val = strAux.replace("_", " ") #solve problem with spaces
            print(val)
        elif(codOp == 14): # GoTo
            pass
        elif(codOp == 15): # GoToF
            pass
        elif(codOp == 16): # GoSub
            pass
        elif(codOp == 17): # endprog
            print("fin del programa :) - Axolotl")
        elif(codOp == 18): # return
            pass
        ip+=1
    

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
        #Reservar memoria global
        if(values[0] == "global"): #tabla global
            listAux = [values[2:5], values[5:]] #lista a reservar
            dicAux = memoriaPrincipal.reservarMemoria("global", listAux)
            memoriaPrincipal.mergeMemories(dicAux) #Agregar reservas a memoria principal    
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
            # testing()
        except EOFError:
            print(EOFError)
    else:
        print(sys.argv[1], ".obj no existente.")