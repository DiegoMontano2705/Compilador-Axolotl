class Memoria:
    
    def Memoria(self):
        self.values = {}
    
    #guardar valor en dic direcciones
    def setVal(self, add, value):
        self.values[add] = value
    
    #Exist value?
    def existVal(self, add):
        return add not in self.values

    #return value
    def getVal(self, add):
        if self.existVal(add):
            print("No existe direccion")
        return self.values[add]
