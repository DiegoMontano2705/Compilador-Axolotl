# 
#     Clase TablaManager: Maneja las tablas y administra mediante dirFun(SuperTabla).
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez 
# 

from Tabla import Tabla

class TablaManager:

    def __init__(self, nameProgram):
        self.nameProgram = nameProgram
        self.dirFun = Tabla("dirFun") #Tabla encargada de administar demas tablas.
        self.currentTablaId = "void" #Tabla en la que se encuentra.
        self.wN = 0 #contador de whiles
        self.fN = 0 #contador de for's

    #sets and gets
    def get_currentTablaId(self):
        return self.currentTablaId

    def set_currentTablaId(self, id):
        self.currentTablaId = id

    def get_wN(self):
        self.wN=self.wN+1
        return self.wN

    def get_fN(self):
        self.fN=self.fN+1
        return self.fN

    #Crea una row en Tabla dir fun.
    def crearTabla(self, id, **kwargs):
        if(not self.dirFun.existRow(id)): #Si no existe se crea la tabla
            tablaAux = Tabla(id)
            self.dirFun.insertRow(id, **kwargs, pointer=tablaAux) #Siempre se va a generar el pointer

    #Al terminar, se elimina dirFun.
    def eraseDirFun(self):
        self.dirFun = Tabla("dirFun")

    #Crea una row en Tabla existente y almacena en tabla interna.
    def insertRowToTabla(self, idTabla, idRow, **kwargs):
        if(not self.getTabla(idTabla).existRow(idRow)):
            self.getTabla(idTabla).insertRow(idRow, **kwargs)
            return True
        print(idRow, " anteriormente declarada en la tabla ", idTabla)
        return False
    
    #Borrar una row en Tabla existente y actualiza en tabla interna.
    def eraseRowToTabla(self, idTabla, idRow):
        if(self.getTabla(idTabla).existRow(idRow)):
            self.getTabla(idTabla).deleteRow(idRow)
            return True
        print(idRow, " no existe en la tabla ", idTabla)
        return False

    #Buscar en que tabla existe la variable.
    def whereExist(self, idRow):
        keys = []
        for key in self.dirFun.getDict():
            if(self.getTabla(key).existRow(idRow)):
                keys.append(key)
        return keys

    #Regresa una tabla en especifico
    def getTabla(self, idTabla):
        return self.dirFun.findRow(idTabla)["pointer"]

    #Testing
    def printDirFun(self):
        self.dirFun.printDic()

    def printTabla(self, idTabla):
        self.getTabla(idTabla).printDic()

def main():
    dirFun = TablaManager("myProgram")
    dirFun.crearTabla("Global", tipo_retorno="void") #Crea una row en tabla dir fun.
    dirFun.crearTabla("Fun1", tipo_retorno="entero")
    print("---dir Fun---")
    dirFun.printDirFun()
    print("---specific tabla---")
    dirFun.insertRowToTabla("Global", "k", tipo="entero")
    dirFun.insertRowToTabla("Global", "x", tipo="float")
    dirFun.insertRowToTabla("Fun1", "k", tipo="float")
    dirFun.getTabla("Fun1").insertRowValue("k", "value", "lol")
    dirFun.getTabla("Fun1").insertRowValue("k", "value", "lol")
    dirFun.eraseRowToTabla("Global", "x")
    dirFun.printTabla("Global")
    dirFun.printTabla("Fun1")
    print(dirFun.whereExist("k"))
    dirFun.eraseDirFun()
    dirFun.printDirFun()

main()

