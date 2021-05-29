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
stackParms = [] #Maneja orden de parametros
stackExe = [] #Maneja el orden de ejecucion
memoriaPrincipal = Memoria() #Maneja la memoria de ejecucion
memorias = [] #Maneja instancias de memorias.
memorias.append(memoriaPrincipal) #Agregar memoria principal
quadruples = [] #Maneja cuadruplos
dirFun  = {} #Recrear dir funciones.
#######################################################   
#Operaciones del programa

#operaciones aritmeticas
def calcula(izq, op, der, dirRes):
    if(op == 1): # +
        memorias[-1].setValMemory(dirRes, (izq + der))
    elif(op == 2): # -
        memorias[-1].setValMemory(dirRes, (izq - der))
    elif(op == 3): # *
        memorias[-1].setValMemory(dirRes, (izq * der))
    elif(op == 4): # /
        memorias[-1].setValMemory(dirRes, (izq / der))
    elif(op == 5): # <
        memorias[-1].setValMemory(dirRes, (izq < der))
    elif(op == 6): # >
        memorias[-1].setValMemory(dirRes, (izq > der))
    elif(op == 7): # <=
        memorias[-1].setValMemory(dirRes, (izq <= der))
    elif(op == 8): # >=
        memorias[-1].setValMemory(dirRes, (izq >= der))
    elif(op == 9): # ==
        memorias[-1].setValMemory(dirRes, (izq == der))
    elif(op == 10): # &
        memorias[-1].setValMemory(dirRes, (izq and der))
    elif(op == 11): # |
        memorias[-1].setValMemory(dirRes, (izq or der))

#######################################################   
#ejecutar programa
def ejecuta():
    memorias.append(memoriaPrincipal) #Agrega memoria global a lista de memorias. index 0.
    ip = 0 #Instruction Pointer
    codOp = int(quadruples[ip][0])

    #Mientras no encuentre fin del programa.
    while codOp != 22: #Mientras no encuentre EndProg
        codOp = int(quadruples[ip][0]) #Codigo de operacion
        if(codOp>=0 and codOp<=11): #operacion aritmetica
            izq = memorias[-1].getValMemory(int(quadruples[ip][1]), memorias[0]) #checar ambas memorias
            der = memorias[-1].getValMemory(int(quadruples[ip][2]), memorias[0])
            res = int(quadruples[ip][3])
            calcula(izq, codOp, der, res)
            ip+=1
        elif(codOp == 12): # =
            val = memorias[-1].getValMemory(int(quadruples[ip][1]), memorias[0])
            res = int(quadruples[ip][3])
            memorias[-1].setValMemory(res, val)
            ip+=1
        elif(codOp == 13): # print
            try: #if not work with value, so its a string
                val = memorias[-1].getValMemory(int(quadruples[ip][3]), memorias[0])  
            except: #work with strings
                strAux = str(quadruples[ip][3:][0])
                val = strAux.replace("_", " ") #solve problem with spaces
            print(val)
            ip+=1
        elif(codOp == 14): # read
            val = input()
            res = int(quadruples[ip][3])
            #checar si va en global o local
            ip+=1
        elif(codOp == 15): # GoTo
            ip = int(quadruples[ip][3]) + 1 #ve directo quad ip.
        elif(codOp == 16): # GoToF
            ip+=1
        elif(codOp == 17): # GoSub
            stackExe.append(ip+1) #Saber a donde tiene que regresar al finalizar func.
            ip = int(quadruples[ip][1])
        elif(codOp == 18): # return
            ip+=1
        elif(codOp == 19): # ERA
            nomFun = quadruples[ip][3]
            rec = dirFun[nomFun]['recursos']
            memoriaAux = Memoria() #Instancia clase
            dicAux = memoriaAux.reservarMemoria("local", rec) #Reserva recursos
            memoriaAux.mergeMemories(dicAux) #Agregar recursos a memoria
            memorias.append(memoriaAux) #Agregas memoria para contexto en ejecucion
            memorias[-1].setDicsAux("local") #Apuntar a los primeros valores.
            stackParms = dirFun[nomFun]['listaParms']
            ip+=1
        elif(codOp == 20): # EndFunc
            memorias.pop() #termina el contexto y se libera memoria local.
            ip = stackExe.pop()
        elif(codOp == 21): # Param
            val = memorias[-1].getValMemory(int(quadruples[ip][1]), memorias[0])
            dirHost = memorias[-1].getDirParm(int(quadruples[ip][1])) #A que dir va
            #Checar tipo 
            if(memorias[-1].getTipoByDir(int(dirHost)) != stackParms[int(quadruples[ip][3])-1]):
                print("Error:", nomFun, "tipo de parametros no coincide con declaracion.")
                sys.exit()
            memorias[-1].setValMemory(dirHost, val) #asigna valor a memoria local del contexto.
            memorias[-1].printMemory()
            ip+=1
        elif(codOp == 22): # endprog
            print("fin del programa :) - Axolotl")
        
    

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
        memorias[0].setValMemory(int(values[0]), values[1])
    #DirFunciones
    for index in range(startDirFun+1, startQuads):
        values = data[index].split()
        #Reservar memoria global
        if(values[0] == "global"): #tabla global
            listAux = [values[2].split("_"), values[3].split("_")] #lista a reservar
            dicAux = memorias[0].reservarMemoria("global", listAux)
            memorias[0].mergeMemories(dicAux) #Agregar reservas a memoria principal   
        else:
            # print(values)
            listaParms = values[4].split("_")
            recVars = values[5].split("_")
            recTmps = values[6].split("_")
            dirFun[values[0]] = {
                'return': values[1],
                'dirInicio':values[2],
                'quadInicio':values[3],
                'listaParms' : listaParms,
                'recursos' : [recVars, recTmps]
            }
             
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
    # rec = dirFun['pruebaDos']['recursos']
    # memAux = memoriaPrincipal.reservarMemoria("local", rec)
    # print(memAux)
    print("###################################################################################")
    print("### Memoria Principal ###")
    memorias[0].printMemory()
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