# 
#     Clase MaquinaVirtual: Ejecuta el archivo obj.
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez 
# 
#######################################################   
from Classes.Quadruples import Quadruples
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
currTabla = [] #Lista de contexto
memoriaObjetos = {} #Memoria para objetos y manejo de su contexto.
currObjeto = "" #Saber con que objeto estoy trabajando.
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

#Asignacion de objetos
def asignacionObjetos(leftOper, rightOper):
    if("_" in leftOper): #variable recibe valor de objeto 
        print("objeto izquierdo")
    elif("_" in rightOper): #se asigna valor a objeto
        direcciones = rightOper.split("_")
        dirObjeto = int(direcciones[0]) #dir objeto
        dirAtributo = int(direcciones[1]) #dirAtributo
        dirValor = int(leftOper) #direccion valor
        valor = memorias[-1].getValMemory(dirValor, memorias[0]) #obtener valor a asignar.
        memoriaObjetos[dirObjeto].setValMemory(dirAtributo, valor)
        # memoriaObjetos[dirObjeto].printMemory()
    else: #asignacion de objeto a objeto
        pass

#######################################################   
#ejecutar programa
def ejecuta():
    memorias.append(memoriaPrincipal) #Agrega memoria global a lista de memorias. index 0.
    ip = 0 #Instruction Pointer
    codOp = int(quadruples[ip][0])
    currTabla.append("global")

    #Mientras no encuentre fin del programa.
    while codOp != 23: #Mientras no encuentre EndProg
        codOp = int(quadruples[ip][0]) #Codigo de operacion

        if(codOp>=0 and codOp<=11): #operacion aritmetica
            if(dirFun[currTabla[-1]]['scope'] == "metodo"): #buscar en memoria local y objetos
                izq = memorias[-1].getValMemory(int(quadruples[ip][1]), memoriaObjetos[int(currObjeto)]) #checar ambas memorias
                der = memorias[-1].getValMemory(int(quadruples[ip][2]), memoriaObjetos[int(currObjeto)])
            else: #buscar en memoria local y global
                izq = memorias[-1].getValMemory(int(quadruples[ip][1]), memorias[0])
                der = memorias[-1].getValMemory(int(quadruples[ip][2]), memorias[0])
            res = int(quadruples[ip][3])
            calcula(izq, codOp, der, res)
            ip+=1
            # memorias[-1].printMemory()
        elif(codOp == 12): # =
            if("_" in quadruples[ip][1] or "_" in quadruples[ip][3]):
                asignacionObjetos(quadruples[ip][1], quadruples[ip][3])
            else: #Si no esta trabajando con objetos
                val = memorias[-1].getValMemory(int(quadruples[ip][1]), memorias[0])
                res = int(quadruples[ip][3])
                memorias[-1].setValMemory(res, val)
            ip+=1
        elif(codOp == 13): # print
            if(dirFun[currTabla[-1]]['scope'] == "metodo"): #en caso de ser objeto
                try: #if not work with value, so its a string
                    val = memorias[-1].getValMemory(int(quadruples[ip][3]), memoriaObjetos[int(currObjeto)]) #checar ambas memorias  
                except: #work with strings
                    strAux = str(quadruples[ip][3:][0])
                    val = strAux.replace("_", " ") #solve problem with spaces
            else:
                try: #if not work with value, so its a string
                    val = memorias[-1].getValMemory(int(quadruples[ip][3]), memorias[0])  
                except: #work with strings
                    strAux = str(quadruples[ip][3:][0])
                    val = strAux.replace("_", " ") #solve problem with spaces
            print(val)
            ip+=1
        elif(codOp == 14): # read
            val = input()
            memorias[-1].setValMemory(int(quadruples[ip][3]), val)
            ip+=1
        elif(codOp == 15): # GoTo
            ipAux = int(quadruples[ip][3])
            if(ipAux < ip): #caso del while.
                ip = ipAux
            else:
                ip = ipAux + 1
        elif(codOp == 16): # GoToF
            #opcio objetos
            val = bool(memorias[-1].getValMemory(int(quadruples[ip][1]), memorias[0]))
            if (not val): #si es falso, ve a quadruplo
                ip = int(quadruples[ip][3])+1
            else:
                ip+=1
        elif(codOp == 17): # GoSub
            stackExe.append(ip+1) #Saber a donde tiene que regresar al finalizar func.
            ip = int(quadruples[ip][1])
        elif(codOp == 18): # return
            if(dirFun[currTabla[-1]]['scope'] == "metodo"):
                val = memorias[-1].getValMemory(int(quadruples[ip][3]), memoriaObjetos[int(currObjeto)])
            else:
                val = memorias[-1].getValMemory(int(quadruples[ip][3]), memorias[0])
            tipo = memorias[-1].getTipoByDir(int(quadruples[ip][3]))
            if(tipo != dirFun[currTabla[-1]]['return']): #validar tipo de retorno
                print("Error: tipo de retorno no coincide con valor regresado.")
                sys.exit()
            #Final de contexto
            # print(val, tipo)
            # memorias[-1].printMemory()
            memorias.pop() #termina el contexto y se libera memoria local.
            currTabla.pop() #Regresa al contexto anterior.
            ip = stackExe.pop() #Sale de la funcion y regresa al quad que sigue.
            memorias[-1].setValMemory(int(quadruples[ip][1]), val) #Asignar valor al temporal return
            
        elif(codOp == 19): # ERA
            currTabla.append(quadruples[ip][3])
            currObjeto = quadruples[ip][1]
            rec = dirFun[currTabla[-1]]['recursos']
            memoriaAux = Memoria() #Instancia clase
            dicAux = memoriaAux.reservarMemoria("local", rec) #Reserva recursos
            memoriaAux.mergeMemories(dicAux) #Agregar recursos a memoria
            memorias.append(memoriaAux) #Agregas memoria para contexto en ejecucion
            memorias[-1].setDicsAux("local") #Apuntar a los primeros valores.
            stackParms = dirFun[currTabla[-1]]['listaParms']
            ip+=1
        elif(codOp == 20): # EndFunc
            # memorias[-1].printMemory()
            memorias.pop() #termina el contexto y se libera memoria local.
            currTabla.pop() #regresa a un contexo antes
            ip = stackExe.pop()
        elif(codOp == 21): # Param
            val = memorias[-1].getValMemory(int(quadruples[ip][1]), memorias[0]) #checar en la memoria local y global.
            if(val == None): #En caso de no encontrar, buscar contexto anterior. Recursividad.
                val = memorias[-2].getValMemory(int(quadruples[ip][1]), memorias[0])
            dirHost = memorias[-1].getDirParm(int(quadruples[ip][1])) #A que dir va
            #Checar tipo 
            if(memorias[-1].getTipoByDir(int(dirHost)) != stackParms[int(quadruples[ip][3])-1]):
                print("Error:", currTabla[-1], "tipo de parametros no coincide con declaracion.")
                sys.exit()
            memorias[-1].setValMemory(dirHost, val) #asigna valor a memoria local del contexto.
            ip+=1
        elif(codOp == 22): #Era objetos
            #Separa memoria para sus atributos.
            rec = dirFun[quadruples[ip][3]]['recursos']
            memoriaAux = Memoria() #Instancia clase
            dicAux = memoriaAux.reservarMemoria("local", rec) #Reserva recursos
            memoriaAux.mergeMemories(dicAux) #Agregar recursos a memoria
            # memoriaAux.printMemory()
            #Guardas memoria con espacios de atributos en la memoria de objetos.
            memoriaObjetos[int(quadruples[ip][1])] = memoriaAux 
            ip+=1
        elif(codOp == 23): # endprog
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
            listAux = [values[1].split("_"), values[2].split("_")] #lista a reservar
            dicAux = memorias[0].reservarMemoria("global", listAux)
            memorias[0].mergeMemories(dicAux) #Agregar reservas a memoria principal 
            dirFun["global"] = {
                'scope':'global'
            }  
        elif(values[0] == "class"): #recrear tabla de clase
            recVars = values[2].split("_")
            recTmps = values[3].split("_")
            dirFun[values[1]] = {
                'scope' : 'clase',
                'recursos' : [recVars, recTmps]
            }
        elif("method_" in values[0]): #recrear tabla method
            listaParms = values[4].split("_")
            recVars = values[5].split("_")
            recTmps = values[6].split("_")
            dirFun[values[1]] = {
                'scope' : 'metodo',
                'clase' : values[0].replace("method_", ""),
                'return' : values[2],
                'quadInicio': values[3],
                'listaParms' : listaParms,
                'recursos' : [recVars, recTmps]
            }
        else:
            listaParms = values[3].split("_")
            recVars = values[4].split("_")
            recTmps = values[5].split("_")
            dirFun[values[0]] = {
                'return': values[1],
                'quadInicio':values[2],
                'listaParms' : listaParms,
                'recursos' : [recVars, recTmps],
                'scope': "funcion"
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