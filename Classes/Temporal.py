# 
#     Clase Temporal: estructura de datos .
#     Compiladores
#     Diego Fernando Montaño Pérez
#     Jose Alberto Gonzalez 
# 

class Temporal:

    def __init__(self):
        self.tmp = set()
        self.len = 0

    #regresa el tmp siguiente y aumenta el contador.
    def next(self):
        val = "tmp"+str(self.len)
        self.tmp.add(val)
        self.len += 1
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

def main():
    t = Temporal()
    t.next()
    idx = t.next()
    t.clearTmp(idx)
    t.next()
    t.next()
    t.printTmp()

main()


