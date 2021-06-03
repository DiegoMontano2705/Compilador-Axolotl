# 
#     Clase Memoria: Crea y maneja direcciones virutales para la memoria.
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez 
# 

#DIRS MEMORIA VIRTUAL
#G=GLOBAL; CTE=CONSTANTE; TMP=TEMPORAL;
#E=ENTERO; F=FLOTANTE; C=CHAR; B=BOOL; 
#INI=INICIA; FIN=TERMINA; 
#Dir Globales 10,000 - 20,499 => 1500 c/u
G_E_INI=10000
G_E_FIN=11499
G_F_INI=11500
G_F_FIN=12999
G_C_INI=13000
G_C_FIN=14499
G_TMP_E_INI=14500
G_TMP_E_FIN=15999
G_TMP_F_INI=16000
G_TMP_F_FIN=17499
G_TMP_C_INI=17500
G_TMP_C_FIN=18999
G_TMP_B_INI=19000
G_TMP_B_FIN=20499
#Dir Constantes 20,500 - 23,499 => 1,000 c/u
CTE_E_INI=20500
CTE_E_FIN=21499
CTE_F_INI=21500
CTE_F_FIN=22499
CTE_C_INI=22500
CTE_C_FIN=23499
#Dir locales 23,500 - 33999 => 1500 c/u
L_E_INI=23500
L_E_FIN=24999
L_F_INI=25000
L_F_FIN=26499
L_C_INI=26500
L_C_FIN=27999
L_TMP_E_INI=28000
L_TMP_E_FIN=29499
L_TMP_F_INI=29500
L_TMP_F_FIN=30999
L_TMP_C_INI=31000
L_TMP_C_FIN=32499
L_TMP_B_INI=32500
L_TMP_B_FIN=33999
#Objetos 34000 - 35999 1,000 c/u
G_OBJETOS_INI = 34000
G_OBJETOS_FIN = 34999
L_OBJETOS_INI = 35000
L_OBJETOS_FIN = 35999

import sys

class Memoria:
    
    def __init__(self):
        self.memory = {}
        #Contadores para aumentar en dics memoria
        self.enterosAux = 0 #enteros
        self.flotantesAux = 0 #flotantes
        self.charAux = 0 #char
        self.tmpEnteroAux = 0 #temporal_entero
        self.tmpFlotanteAux = 0 #temporal_flotante
        self.tmpCharAux = 0 #temporal_char
        self.tmpBoolAux = 0 #tempora_bool\
        self.objetoAux = 0 #objeto


#######################################################      
    #set dirs en auxiliares
    def setDicsAux(self, tipoMemoria):
        if tipoMemoria == "global":
            self.enterosAux = G_E_INI
            self.flotantesAux = G_F_INI
            self.charAux = G_C_INI
            self.tmpEnteroAux = G_TMP_E_INI
            self.tmpFlotanteAux = G_TMP_F_INI
            self.tmpCharAux = G_TMP_C_INI
            self.tmpBoolAux = G_TMP_B_INI
            self.objetoAux = G_OBJETOS_INI
        elif tipoMemoria == "constantes":
            self.enterosAux = CTE_E_INI
            self.flotantesAux = CTE_F_INI
            self.charAux = CTE_C_INI
        elif tipoMemoria == "local":
            self.enterosAux = L_E_INI
            self.flotantesAux = L_F_INI
            self.charAux = L_C_INI
            self.tmpEnteroAux = L_TMP_E_INI
            self.tmpFlotanteAux = L_TMP_F_INI
            self.tmpCharAux = L_TMP_C_INI
            self.tmpBoolAux = L_TMP_B_INI
            self.objetoAux = L_OBJETOS_INI
    

#######################################################
    #guardar valor en dic direcciones
    #tipo = entero, flotante, char, bool
    #contexto = vars o tmps
    def setGlobalVal(self, value, tipo, contexto):
        if(contexto == "vars"): #Variables
            if(tipo == "entero"):
                if self.enterosAux in range(G_E_INI, G_E_FIN):
                    self.memory[self.enterosAux] = value
                    self.enterosAux+=1
                else:
                    print("overflow memoria: globales enteras.")
                    sys.exit()
            elif(tipo == "flotante"):
                if self.flotantesAux in range(G_F_INI, G_F_FIN):
                    self.memory[self.flotantesAux] = value
                    self.flotantesAux+=1
                else:
                    print("overflow memoria: globales flotante.")
                    sys.exit()
            elif(tipo == "char"):
                if self.charAux in range(G_C_INI, G_C_FIN):
                    self.memory[self.charAux] = value
                    self.charAux+=1
                else:
                    print("overflow memoria: globales chars.")
                    sys.exit()
            else:
                if self.objetoAux in range(G_OBJETOS_INI, G_OBJETOS_FIN):
                    self.memory[self.objetoAux] = value
                    self.objetoAux+=1
                else:
                    print("overflow memoria: globales objetos.")
                    sys.exit()
        elif(contexto == "tmps"): #temporales
            if(tipo=="entero"):
                if self.tmpEnteroAux in range(G_TMP_E_INI, G_TMP_E_FIN):
                    self.memory[self.tmpEnteroAux] = value
                    self.tmpEnteroAux+=1
                    return (self.tmpEnteroAux-1)
                else:
                    print("overflow memoria: temporales globales enteras.")
                    sys.exit()
            elif(tipo=="flotante"):
                if self.tmpFlotanteAux in range(G_TMP_F_INI, G_TMP_F_FIN):
                    self.memory[self.tmpFlotanteAux] = value
                    self.tmpFlotanteAux+=1
                    return (self.tmpFlotanteAux-1)
                else:
                    print("overflow memoria: temporales globales flotantes.")
                    sys.exit()
            elif(tipo=="char"):
                if self.tmpCharAux in range(G_TMP_C_INI, G_TMP_C_FIN):
                    self.memory[self.tmpCharAux] = value
                    self.tmpCharAux+=1
                    return (self.tmpCharAux-1)
                else:
                    print("overflow memoria: temporales globales chars.")
                    sys.exit()
            elif(tipo=="bool"):
                if self.tmpBoolAux in range(G_TMP_B_INI, G_TMP_B_FIN):
                    self.memory[self.tmpBoolAux] = value
                    self.tmpBoolAux+=1
                    return (self.tmpBoolAux-1)
                else:
                    print("overflow memoria: temporales globales chars.")
                    sys.exit()
#######################################################
    #guardar valor en dic que no se repita
    #constantes
    def setConstante(self, value):
        if(value not in (self.memory.values())):
            if(isinstance(value, int)):
                if self.enterosAux in range(CTE_E_INI, CTE_E_FIN):
                    self.memory[self.enterosAux] = int(value)
                    self.enterosAux+=1
                else:
                    print("overflow memoria: constantes enteras.")
                    sys.exit()
            elif(isinstance(value, float)):
                if self.flotantesAux in range(CTE_F_INI, CTE_F_FIN):
                    self.memory[self.flotantesAux] = float(value)
                    self.flotantesAux+=1
                else:
                    print("overflow memoria: constantes flotantes.")
                    sys.exit()
            elif(isinstance(value, str)):
                if self.charAux in range(CTE_C_INI, CTE_C_FIN):
                    self.memory[self.charAux] = str(value)
                    self.charAux+=1
                else:
                    print("overflow memoria: constantes chars.")
                    sys.exit()
            else:
                print("type mismatch: constantes solo enteras, flotante, char.")
    
#######################################################
#Locales
#Regresa direccion virutal para las vars y temporales locales dentro de un contexto.

    #get only local dir
    def getLocalDirVirtual(self, tipo, contexto):
            if(contexto == "vars"): #Variables
                if(tipo == "entero"):
                    if self.enterosAux in range(L_E_INI, L_E_FIN):
                        self.enterosAux+=1
                        return (self.enterosAux-1)
                    else:
                        print("overflow memoria: locales enteras.")
                        sys.exit()
                elif(tipo == "flotante"):
                    if self.flotantesAux in range(L_F_INI, L_F_FIN):
                        self.flotantesAux+=1
                        return (self.flotantesAux-1)
                    else:
                        print("overflow memoria: locales flotantes.")
                        sys.exit()
                elif(tipo == "char"):
                    if self.charAux in range(L_C_INI, L_C_FIN):
                        self.charAux+=1
                        return (self.charAux-1)
                    else:
                        print("overflow memoria: locales chars.")
                        sys.exit()
                else:
                    if self.objetoAux in range(L_OBJETOS_INI, L_OBJETOS_FIN):
                        self.objetoAux+=1
                        return (self.objetoAux-1)
                    else:
                        print("overflow memoria: locales objetos.")
                        sys.exit()
            elif(contexto == "tmps"): #temporales
                if(tipo=="entero"):
                    if self.tmpEnteroAux in range(L_TMP_E_INI, L_TMP_E_FIN):
                        self.tmpEnteroAux+=1
                        return (self.tmpEnteroAux-1)
                    else:
                        print("overflow memoria: temporales locales enteras.")
                        sys.exit()
                elif(tipo=="flotante"):
                    if self.tmpFlotanteAux in range(L_TMP_F_INI, L_TMP_F_FIN):
                        self.tmpFlotanteAux+=1
                        return (self.tmpFlotanteAux-1)
                    else:
                        print("overflow memoria: temporales locales flotantes.")
                        sys.exit()
                elif(tipo=="char"):
                    if self.tmpCharAux in range(L_TMP_C_INI, L_TMP_C_FIN):
                        self.tmpCharAux+=1
                        return (self.tmpCharAux-1)
                    else:
                        print("overflow memoria: temporales locales chars.")
                        sys.exit()
                elif(tipo=="bool"):
                    if self.tmpBoolAux in range(L_TMP_B_INI, L_TMP_B_FIN):
                        self.tmpBoolAux+=1
                        return (self.tmpBoolAux-1)
                    else:
                        print("overflow memoria: temporales locales chars.")
                        sys.exit()

#######################################################
    #Reset contadores/pointers a memoria.
    def reseteRecursos(self):
        self.enterosAux=0
        self.flotantesAux=0
        self.charAux=0
        self.tmpEnteroAux=0
        self.tmpFlotanteAux=0
        self.tmpCharAux=0
        self.tmpBoolAux=0
#######################################################
#Auxiliares Memoria

    #Regresa direccion de un variable/cte especifico
    def getDirMemory(self, id):
        try:
            key_list = list(self.memory.keys())
            val_list = list(self.memory.values())
            if(isinstance(id, int)):
                position = val_list.index(int(id))
            elif(isinstance(id, float)):
                position = val_list.index(float(id))
            elif(isinstance(id, str)):
                position = val_list.index(str(id))
        except ValueError:
            print("ERROR:",id, "no encontrado ni local y global")
            sys.exit()
        return key_list[position], self.getTipoByDir(key_list[position])

    def getTipoByDir(self, dir):
        if(int(dir) in range(G_E_INI, G_E_FIN) or int(dir) in range(L_E_INI, L_E_FIN) or int(dir) in range(G_TMP_E_INI, G_TMP_E_FIN) or int(dir) in range(L_TMP_E_INI, L_TMP_E_FIN) or int(dir) in range(CTE_E_INI, CTE_E_FIN)):
            return "entero"
        elif(int(dir) in range(G_F_INI, G_F_FIN) or int(dir) in range(L_F_INI, L_F_FIN)or int(dir) in range(G_TMP_F_INI, G_TMP_F_FIN) or int(dir) in range(L_TMP_F_INI, L_TMP_F_FIN) or int(dir) in range(CTE_F_INI, CTE_F_FIN)):
            return "flotante"
        elif(int(dir) in range(G_C_INI, G_C_FIN) or int(dir) in range(L_C_INI, L_C_FIN)or int(dir) in range(G_TMP_C_INI, G_TMP_C_FIN) or int(dir) in range(L_TMP_C_INI, L_TMP_C_FIN) or int(dir) in range(CTE_C_INI, CTE_C_FIN)):
            return "char"
        elif(int(dir) in range(G_TMP_B_INI, G_TMP_B_FIN) or int(dir) in range(L_TMP_B_INI, L_TMP_B_FIN)):
            return "bool"
#######################################################
#Memoria de ejecucion

    #Reservar memoria con direcciones con formato [[entero,flotante,char],[tmpEntero, tmpflotante, tmpChar, tmpBool]]
    #tipoMemoria = global o local
    #contexto = vars o tmps
    def reservarMemoria(self, tipoMemoria, listaTipos):
        memoriaAux = Memoria()
        memoriaAux.setDicsAux(tipoMemoria)
        if(tipoMemoria == "global"):
            for i in range(0, int(listaTipos[0][0])): #reservar globales enteras
                memoriaAux.setGlobalVal(None, "entero", "vars")
            for i in range(0, int(listaTipos[0][1])): #reservar globales flotante
                memoriaAux.setGlobalVal(None, "flotante", "vars")
            for i in range(0, int(listaTipos[0][2])): #reservar globales char
                memoriaAux.setGlobalVal(None, "char", "vars")
            for i in range(0, int(listaTipos[1][0])): #reservar globales temporal enteras
                memoriaAux.setGlobalVal(None, "entero", "tmps")
            for i in range(0, int(listaTipos[1][1])): #reservar globales temporal flotante
                memoriaAux.setGlobalVal(None, "flotante", "tmps")
            for i in range(0, int(listaTipos[1][2])): #reservar globales temporal char
                memoriaAux.setGlobalVal(None, "char", "tmps")
            for i in range(0, int(listaTipos[1][3])): #reservar globales temporal bool
                memoriaAux.setGlobalVal(None, "bool", "tmps")
            return (memoriaAux.getMemory()) #Regresa memoria con direcciones reservadas
        elif(tipoMemoria == "local"): #Memoria local.
            for i in range(0, int(listaTipos[0][0])): #reservar locales enteras
                dirAux = memoriaAux.getLocalDirVirtual("entero", "vars") #get local dir
                memoriaAux.setValMemory(int(dirAux), None) #asginar 
            for i in range(0, int(listaTipos[0][1])): #reservar locales flotante
                dirAux = memoriaAux.getLocalDirVirtual("flotante", "vars") #get local dir
                memoriaAux.setValMemory(int(dirAux), None)
            for i in range(0, int(listaTipos[0][2])): #reservar locales char
                dirAux = memoriaAux.getLocalDirVirtual("char", "vars") #get local dir
                memoriaAux.setValMemory(int(dirAux), None)
            for i in range(0, int(listaTipos[1][0])): #reservar locales temporal enteras
                dirAux = memoriaAux.getLocalDirVirtual("entero", "tmps") #get local dir
                memoriaAux.setValMemory(int(dirAux), None)
            for i in range(0, int(listaTipos[1][1])): #reservar locales temporal flotante
                dirAux = memoriaAux.getLocalDirVirtual("flotante", "tmps") #get local dir
                memoriaAux.setValMemory(int(dirAux), None)
            for i in range(0, int(listaTipos[1][2])): #reservar locales temporal char
                dirAux = memoriaAux.getLocalDirVirtual("char", "tmps") #get local dir
                memoriaAux.setValMemory(int(dirAux), None)
            for i in range(0, int(listaTipos[1][3])): #reservar locales temporal bool
                dirAux = memoriaAux.getLocalDirVirtual("bool", "tmps") #get local dir
                memoriaAux.setValMemory(int(dirAux), None)
            return (memoriaAux.getMemory()) #Regresa memoria con direcciones reservadas
        else:
            print("Error:", tipoMemoria, "no valido.")
            sys.exit()
    
    #Juntar dos memorias (merge dictionaries)
    def mergeMemories(self, dict1):
        self.memory.update(dict1)

    #Regresar valores guardados
    def getMemory(self):
        return self.memory

    #Regresa direccion que le corresponde depende el tipo.
    def getDirParm(self, dir):
        tipo = self.getTipoByDir(int(dir))
        if(tipo == "entero"): #regresa la variable entera que le corresponde
            self.enterosAux+= 1
            return self.enterosAux - 1 
        elif(tipo == "flotante"):
            self.flotantesAux+=1
            return self.flotantesAux - 1
        elif(tipo == "char"):
            self.charAux+=1
            return self.charAux - 1

    #Regresa valor dada una direccion buscando en local y global
    def getValMemory(self, dir, memoriaGlobal):
        if dir in self.memory:
            return self.memory[dir]
        elif( dir in memoriaGlobal.memory):
            return memoriaGlobal.memory[dir]
        else:
            print("Error:",dir,"no existente en la memoria ejecucion local ni global.")
            sys.exit()

    #Set valor en una direccion
    def setValMemory(self, dir, value):
        if(value == None):
            self.memory[dir] = None
        elif(self.getTipoByDir(dir) == "entero"):
            self.memory[dir] = int(value)
        elif(self.getTipoByDir(dir) == "flotante"):
            self.memory[dir] = float(value)
        elif(self.getTipoByDir(dir) == "char"):
            self.memory[dir] = str(value)
        elif(self.getTipoByDir(dir) == "bool"):
            self.memory[dir] = bool(value)
        else:
            print("Error:",dir, "fuera de rango de memoria.")

##############################################################################################################
#Testing    
    #print memory
    def printMemory(self):
        print(self.memory)

# def main():
#     m = Memoria()
#     m.setDicsAux("local")
#     print(m.getLocalDirVirtual("entero", "vars"))
#     print(m.getLocalDirVirtual("entero", "vars"))
#     print(m.getLocalDirVirtual("entero", "vars"))

# main()