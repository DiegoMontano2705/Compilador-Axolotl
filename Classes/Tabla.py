# 
#     Clase Tabla: estructura de datos para almacenar informacion tablas.
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez 
# 

class Tabla:

    def __init__(self, id_tabla):
        self.id_tabla=id_tabla
        self.dict = {}

    def getDict(self):
        return self.dict

    def nameTable(self):
        return self.id_tabla

    def insertRow(self,id, **kwargs):
        self.dict[id] = {}
        for key, value in kwargs.items():
            self.dict[id][key] = value

    def deleteRow(self, id):
        if(self.dict.pop(id, None)):
            return True
        return False

    def findRow(self, id):
        if id in self.dict:
            return self.dict[id]

    def existRow(self, id):
        if id in self.dict:
            return True
        return False

    def updateRow(self, id, **kwargs):
        if(self.findRow(id)):
            self.dict[id] = {}
            for key, value in kwargs.items():
                self.dict[id][key] = value
            return True
        return False

    def updateRowValue(self, tableId, atributeId, newValue):
        if(self.findRow(tableId)):
            self.dict[tableId][atributeId] = newValue
            return True
        return False

    def printDic(self):
        print(self.dict)
