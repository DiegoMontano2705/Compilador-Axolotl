# 
#     Clase TablaManager: Maneja las tablas y administra mediante dirFun(SuperTabla).
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez 
# 

from Tabla import Tabla

class TablaManager:

    def __init__(self):
        self.dirFun = Tabla("dirFun") #Tabla encargada de administar demas tablas.

    def printDirFun(self):
        self.dirFun.printDic()
    
    #Crea una row en Tabla dir fun.
    def crearTabla(self, id, **kwargs):
        if(not self.dirFun.existRow(id)): #Si no existe se crea la tabla
            tablaAux = Tabla(id)
            self.dirFun.insertRow(id, **kwargs, pointer=tablaAux) #Siempre se va a generar el pointer

    #Crea una row en Tabla existente y almacena en tabla interna.
    def insertRowToTabla(self, idTabla, idRow, **kwargs):
        if(not self.getTabla(idTabla).existRow(idRow)):
            self.getTabla(idTabla).insertRow(idRow, **kwargs)
            return True
        return False
    
    #Borrar una row en Tabla existente y actualiza en tabla interna.
    def eraseRowToTabla(self, idTabla, idRow):
        if(self.getTabla(idTabla).existRow(idRow)):
            self.getTabla(idTabla).deleteRow(idRow)
            return True
        return False

    #Buscar en que tabla existe la variable.
    def whereExist(self, idRow):
        keys = []
        for key in self.dirFun.getDict():
            if(self.getTabla(key).existRow(idRow)):
                keys.append(key)
        return keys

    def printTabla(self, idTabla):
        self.getTabla(idTabla).printDic()

    #Regresa una tabla en especifico
    def getTabla(self, idTabla):
        return self.dirFun.findRow(idTabla)["pointer"]

    #TODO: 
    #son del mismo tipo?
    # def sameType(self, idTabla, *args):
    # types = []
    #     for idVar in args:
    #         self.getTabla(idTabla).
    # result = all(element == List[0] for element in List)

def main():
    dirFun = TablaManager()
    dirFun.crearTabla("Global", tipo_retorno="void") #Crea una row en tabla dir fun.
    dirFun.crearTabla("Fun1", tipo_retorno="entero")
    print("---dir Fun---")
    dirFun.printDirFun()
    print("---specific tabla---")
    dirFun.insertRowToTabla("Global", "k", tipo="entero")
    dirFun.insertRowToTabla("Global", "x", tipo="float")
    dirFun.insertRowToTabla("Fun1", "k", tipo="float")
    dirFun.eraseRowToTabla("Global", "x")
    dirFun.printTabla("Global")
    print(dirFun.whereExist("k"))

    
main()

