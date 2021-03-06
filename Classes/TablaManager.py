# 
#     Clase TablaManager: Maneja las tablas y administra mediante dirFun(SuperTabla).
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez 
# 

from re import L
from typing import List
from Classes.Tabla import *
from Classes.Memoria import *

class TablaManager:

    def __init__(self):
        self.dirFun = Tabla("dirFun") #Tabla encargada de administar demas tablas.
        self.currentScope = "global" #En que scope se encuentra: class or global
        self.currentTablaId = "global" #Tabla en la que se encuentra.
        self.currentType = None #Que tipo de variable se encuentra.
        self.nombrePrograma = None #Nombre del programa
        
######################################################################################
    #sets and gets
    def get_currentTablaId(self):
        return self.currentTablaId

    def set_currentTablaId(self, id):
        self.currentTablaId = id

    def set_nombrePrograma(self, id):
        self.nombrePrograma = id
        
    def get_nombrePrograma(self):
        return self.nombrePrograma

    def get_currentType(self):
        return self.currentType

    def set_currentType(self, id):
        self.currentType = id

    def get_currentScope(self):
        return self.currentScope

    def set_currentScope(self, id):
        self.currentScope = id
    
######################################################################################
#CRUD TABLAS

    #Crea una row en Tabla dir fun.
    def crearTabla(self, id, **kwargs):
        if(not self.dirFun.existRow(id)): #Si no existe se crea la tabla
            tablaAux = Tabla(id)
            listaParms = list() #Crear lista orden tipo de parametros.
            dicObjetos = dict() #diccionario para contar objetos
            memoriaLocal = Memoria() #manejar memoria con dirs para vars.
            memoriaLocal.setDicsAux("local")
            self.dirFun.insertRow(id, **kwargs, recursos={"vars":[0,0,0],"tmps":[0,0,0,0]},tablaVar=tablaAux, listaParms=listaParms, memoriaLocal=memoriaLocal, dicObjetos=dicObjetos) #Siempre se va a generar el pointer
    

    #Al terminar, se elimina dirFun.
    def deleteTablaVars(self, idTabla):
        if(self.dirFun.existRow(idTabla)):
            self.getTablaVar(idTabla).deleteTabla() #Eliminar tabla
            self.dirFun.findRow(idTabla).pop("tablaVar") #Eliminar de dictionary.

######################################################################################
    #Add reserva de recursos en contexto
    # [enteros, flotantes, chars] [enteros,flotantes,chars,bool]
    def addContRecursos(self, idTabla, tipo):
        if(tipo == "entero"):
            self.dirFun.findRow(idTabla)["recursos"]["vars"][0] = self.dirFun.findRow(idTabla)["recursos"]["vars"][0]+1
        elif(tipo=="flotante"):
            self.dirFun.findRow(idTabla)["recursos"]["vars"][1] = self.dirFun.findRow(idTabla)["recursos"]["vars"][1]+1
        elif(tipo=="char"):
            self.dirFun.findRow(idTabla)["recursos"]["vars"][2] = self.dirFun.findRow(idTabla)["recursos"]["vars"][2]+1
        else: #contador para objetos
            if(tipo not in self.dirFun.findRow(idTabla)["dicObjetos"]):
                self.dirFun.findRow(idTabla)["dicObjetos"][tipo] = 1
            else:
                self.dirFun.findRow(idTabla)["dicObjetos"][tipo] = self.dirFun.findRow(idTabla)["dicObjetos"][tipo] + 1

    #Asigna lista de recursos temporales por contexto
    def setListaTemporales(self, idTabla, listaTmps):
        self.dirFun.findRow(idTabla)["recursos"]["tmps"] = listaTmps 

    #Regresa recursos utilizados por contexto.
    def getRecursos(self, idTabla):
        return self.dirFun.findRow(idTabla)["recursos"]

    #Regresa quad inicio de funcion especificada
    def getQuadIni(self, idTabla):
        return self.dirFun.findRow(idTabla)['quadIni']
    
    #Regresa tipo de retorno de la funcion
    def getTipoRetornoFun(self, idTabla):
        return self.dirFun.findRow(idTabla)['retorno']

    #Regresa scope de la funcion
    def getScopeFun(self, idTabla):
        return self.dirFun.findRow(idTabla)['scope']

######################################################################################
#Manejo TablaVars
    #Crea una row en Tabla existente y almacena en tabla interna.
    def insertRowToTablaVar(self, idTabla, idRow, tip, contexto, **kwargs):
        if(not self.getTablaVar(idTabla).existRow(idRow)):
            #Agregar dir a variable por contexto.
            memoriaLocal = self.getMemoriaLocal(idTabla) 
            dirAux = memoriaLocal.getLocalDirVirtual(tip, contexto)
            self.getTablaVar(idTabla).insertRow(idRow, tipo=tip, dirVirtual=dirAux, **kwargs)
            return True
        print(idRow, " anteriormente declarada en la tabla ", idTabla)
        return False
    
    #Agregar tipo a la lista de paraemtros de una tabla especificada.
    def insertRowToListaParms(self, idTabla, tipo):
        self.dirFun.findRow(idTabla)["listaParms"].append(tipo)
    
    #Borrar una row en Tabla existente y actualiza en tabla interna.
    def eraseRowToTablaVar(self, idTabla, idRow):
        if(self.getTablaVar(idTabla).existRow(idRow)):
            self.getTablaVar(idTabla).deleteRow(idRow)
            return True
        print(idRow, " no existe en la tabla ", idTabla)
        return False
    

    #Buscar en que tabla existe la variable.
    def whereExistTablaVar(self, idRow):
        keys = []
        for key in self.dirFun.getDict():
            if(self.getTablaVar(key).existRow(idRow)):
                keys.append(key)
        return keys

    #Regresa una tabla en especifico
    def getTablaVar(self, idTabla):
        return self.dirFun.findRow(idTabla)["tablaVar"]

    #Regresa tipo de una variable especifica en tablaVariables especificada
    def getTipoIdTablaVars(self, idTabla, idVar):
        currTabla = self.getTablaVar(idTabla)
        if(currTabla.findRow(idVar)):
            return currTabla.findRow(idVar)["tipo"]

    #Regresa dir memoria virtual especifica en tablaVariables especificada
    def getDirIdTablaVars(self, idTabla, idVar):
        currTabla = self.getTablaVar(idTabla)
        if(currTabla.findRow(idVar)):
            return currTabla.findRow(idVar)["dirVirtual"]
        else:
            return -1

    #Regresa memoria en especifico
    def getMemoriaLocal(self, idTabla):
        return (self.dirFun.findRow(idTabla)["memoriaLocal"])

    #Regresa lista de tipos de parametros de una tabla especificada.
    def getListaParms(self, idTabla):
        self.dirFun.findRow(idTabla)["listaParms"].reverse() #Reverse para el orden correcto
        return self.dirFun.findRow(idTabla)["listaParms"]
    
    #Set lista de tipos parametros de una tabla especificada
    def setListaParms(self, idTabla):
        self.dirFun.findRow(idTabla)["listaParms"].reverse() #Reverse para el orden correcto

######################################################################################
    #Testing
    def printDirFun(self):
        self.dirFun.printDic()

    #print tabla vars
    def printTablaVars(self, idTabla):
        self.getTablaVar(idTabla).printDic()
    #print tabla parms
    def printListaParms(self, idTabla):
        print(self.getListaParms(idTabla))

# def main():
#     dirFun = TablaManager("myProgram")
#     dirFun.crearTabla("Global", tipo_retorno="void", dirInicio=20000, recursos=[1, 2, 3]) #Crea una row en tabla dir fun.
#     dirFun.crearTabla("Fun1", tipo_retorno="entero", dirInicio=20000, recursos=[1, 2, 3], pointer_tablaParams="<dir>")
#     print("---dir Fun---")
#     dirFun.printDirFun()
#     print("---specific tabla---")
#     dirFun.insertRowToTabla("Global", "k", tipo="entero", dirVirutal=1001)
#     dirFun.insertRowToTabla("Global", "x", tipo="flotante", dirVirutal=2001)
#     dirFun.insertRowToTabla("Fun1", "k", tipo="flotante", dirVirutal=2002)
#     dirFun.getTabla("Fun1").insertRowValue("k", "value", "lol")
#     dirFun.getTabla("Fun1").insertRowValue("k", "value", "lol")
#     dirFun.eraseRowToTabla("Global", "x")
#     dirFun.printTabla("Global")
#     dirFun.printTabla("Fun1")
#     print(dirFun.whereExist("k"))
#     dirFun.eraseDirFun()
#     dirFun.printDirFun()

# main()

