# 
#     Clase Tabla: estructura de datos para almacenar informacion tablas.
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez 
# 
import sys
class Tabla:

    def __init__(self, id_tabla):
        self.id_tabla=id_tabla
        self.dict = {}

    def getDict(self):
        return self.dict

    def nameTable(self):
        return self.id_tabla

    def deleteTabla(self):
        self.id_tabla=""
        self.dict.clear()

    #Agrega una nueva row con id y los kwargs pasados.
    def insertRow(self,id, **kwargs):
        self.dict[id] = {}
        for key, value in kwargs.items():
            self.dict[id][key] = value

    #Agrega un nuevo atributo a la row especificada id.
    def insertRowValue(self, idRow, id, value):
        if (not self.existRowValue(idRow, id)):
            self.dict[idRow][id]=value
            return True
        print(id, " ya existente en ", idRow)
        return False

    #Elimina completamente la row id.
    def deleteRow(self, id):
        if(self.dict.pop(id, None)):
            return True
        print(id, " no existente.")
        return False

    #Regresa la row especificada.
    def findRow(self, id):
        if id in self.dict:
            return self.dict[id]
        else:
            return None

    #Regresa true/false para ver si existe la row en la tabla.
    def existRow(self, id):
        if id in self.dict:
            return True
        return False

    #Regresa true/false para ver si existe el argumento en el row.
    def existRowValue(self, idRow, id):
        if id in self.dict[idRow]:
            return True
        return False

    #Actualiza la tabla id con los argumentos en kwargs.
    def updateRow(self, id, **kwargs):
        if(self.findRow(id)):
            self.dict[id] = {}
            for key, value in kwargs.items():
                self.dict[id][key] = value
            return True
        print(id, " no existente.")
        return False

    #Actualiza el atributo de la row con el nuevo valor.
    def updateRowValue(self, tableId, atributeId, newValue):
        if(self.findRow(tableId)):
            self.dict[tableId][atributeId] = newValue
            return True
        print(atributeId, " no existente en la tabla ", tableId)
        return False

    def printDic(self):
        for key, values in self.dict.items():
            print("--------------------------------------------")
            print(key, values)

