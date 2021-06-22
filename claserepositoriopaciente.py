from clasepaciente import Paciente
from clasemanejadorpaciente import manejapacientes
from claseobject import ObjectEncoder

class repositoriopaciente:
    __enco = None
    __manejador = None

    def __init__(self,enco):
        self.__enco = enco
        lista = self.__enco.leerJSONArchivo()
        self.__manejador = manejapacientes()
        self.__manejador.decodificarLista(lista)

    def obtenerlistapa(self):
        return self.__manejador.listarpa()

    def agregar(self,paciente):
        self.__manejador.agregar(paciente)
        return paciente
    def modificapa(self,paciente):
        self.__manejador.actualizarpa(paciente)
        return paciente
    def borrapa(self,paciente):
        self.__manejador.eliminarpa(paciente)

    def grabarDatos(self):
        lista = self.__manejador.toJSON()
        self.__enco.guardarJSONArchivo(lista)