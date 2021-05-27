# 
#     Clase Temporal: estructura de datos para la administracion de espacios en memoria para los temporales.
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez 
# 
from Classes.Memoria import *

class Temporal:

    def __init__(self):
        self.tmp = set()
        self.len = 0
        self.lastContext = ""
        self.memoriaLocal = Memoria()
        self.memoriaLocal.setDicsAux("local")
        self.memoriaGlobal = Memoria()
        self.memoriaGlobal.setDicsAux("global")

    #regresa el tmp siguiente y aumenta el contador.
    #contexto global o local
    def next(self, tipo, contexto):
        #Utilizando strings
        # val = "tmp_"+str(tipo)+"_"+str(self.len)
        # self.tmp.add(val)
        # self.len += 1
        #Utilizando dirs memoria
        if(contexto == "global"):
            val = self.memoriaGlobal.setGlobalVal("", tipo, "tmps") #dir temporal global
        elif(contexto == self.lastContext):
            val= self.memoriaLocal.getLocalDirVirtual(tipo, "tmps") #dir temporal local
        else: 
            self.lastContext = contexto
            self.memoriaLocal.setDicsAux("local") #reset dirs locales cambio de contexto
            val = self.memoriaLocal.getLocalDirVirtual(tipo, "tmps")
        return val

    #clearTmp(idTmp) elimina el idTmp del diccionario.
    def clearTmp(self, idTmp):
        self.tmp.remove(idTmp)
    
    #clear() limpiar toda el set y el contador.
    def clear(self):
        self.len=0
        self.tmp.clear()

    #return len
    def getLen(self):
        return self.len

    #print tmp
    def printTmp(self):
        print(self.tmp)

# def main():
#     t = Temporal()
#     t.next()
#     idx = t.next()
#     t.clearTmp(idx)
#     t.next()
#     t.next()
#     t.printTmp()

# main()


