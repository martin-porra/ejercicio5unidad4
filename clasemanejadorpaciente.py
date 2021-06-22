from clasepaciente import Paciente

class manejapacientes:
    indice = 0
    __pacientes = None

    def __init__(self):
        self.__pacientes = []

    def agregar(self,paciente):
        paciente.rowid = manejapacientes.indice
        manejapacientes.indice += 1
        self.__pacientes.append(paciente)

    def listarpa(self):
        return self.__pacientes

    def eliminarpa(self,paciente):
        indice = self.getidpaciente(paciente)
        self.__pacientes.pop(indice)

    def actualizarpa(self,paciente):
        indice = self.getidpaciente(paciente)
        self.__pacientes[indice] = paciente

    def getidpaciente(self,paciente):
        bandera = False
        i = 0
        while i < len(self.__pacientes) and not bandera:
            if self.__pacientes[i].rowid == paciente.rowid:
                bandera = True
            else:
                i += 1
        return i

    def toJSON(self):
        lista = [paciente.toJSON() for paciente in self.__pacientes]
        return lista

    def decodificarLista(self, lista):
        for paciente in lista:
            class_name=paciente['__class__']
            class_=eval(class_name)
            atributos=paciente['__atributos__']
            nuevopa=class_(**atributos)
            self.agregar(nuevopa)