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
        self.tmpGlobalEntero = 0
        self.tmpGlobalFloat = 0
        self.tmpGlobalChar = 0
        self.tmpGlobalBool = 0
        self.tmpLocalEntero = 0
        self.tmpLocalFloat = 0
        self.tmpLocalChar = 0
        self.tmpLocalBool = 0

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
            #contadores de temporales globales
            if(tipo=="entero"):
                self.tmpGlobalEntero+=1
            elif(tipo=="float"):
                self.tmpGlobalFloat+=1
            elif(tipo=="char"):
                self.tmpGlobalChar+=1
            elif(tipo=="bool"):
                self.tmpGlobalBool+=1
            else:
                print("Error:",tipo," no valido.")
        else:
            if(contexto == self.lastContext):
                val= self.memoriaLocal.getLocalDirVirtual(tipo, "tmps") #dir temporal local
            else: 
                self.lastContext = contexto
                self.memoriaLocal.setDicsAux("local") #reset dirs locales cambio de contexto
                self.resetTmpsLocales() #reset contadores locales de temporales.
                val = self.memoriaLocal.getLocalDirVirtual(tipo, "tmps")
            if(tipo=="entero"):
                self.tmpLocalEntero+=1
            elif(tipo=="float"):
                self.tmpLocalFloat+=1
            elif(tipo=="char"):
                self.tmpLocalChar+=1
            elif(tipo=="bool"):
                self.tmpLocalBool+=1
            else:
                print("Error:",tipo," no valido.")
        return val


    #reset contadores
    def resetTmpsLocales(self):
        self.tmpLocalEntero=0
        self.tmpLocalFloat=0
        self.tmpLocalChar=0
        self.tmpLocalBool=0

    #get recursos de temporales locales
    def getListaTemporalesLocales(self):
        tE = self.tmpLocalEntero
        tF = self.tmpLocalFloat
        tC = self.tmpLocalChar
        tB = self.tmpLocalBool
        return [tE, tF, tC, tB]

    #get recursos de temporales globales
    def getListaTemporalesGlobales(self):
        tE = self.tmpGlobalEntero
        tF = self.tmpGlobalFloat
        tC = self.tmpGlobalChar
        tB = self.tmpGlobalBool
        return [tE, tF, tC, tB]


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


