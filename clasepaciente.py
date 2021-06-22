class Paciente():
    __nombre = ''
    __apellido = ''
    __telefono = ''
    __altura = 0
    __peso = 0

    def __init__(self,nombre,apellido,telefono,altura,peso):
        self.__nombre = self.reque(nombre, 'se requiere Nombre')
        self.__apellido = self.reque(apellido, 'se requiere Apellido')
        self.__telefono = self.reque(telefono, 'se requiere telefono')
        self.__altura = self.reque(altura, 'se requiere Altura')
        self.__peso = self.reque(peso, 'se requiere Peso')

    def getNombre(self):
        return self.__nombre
    def getApellido(self):
        return self.__apellido
    def getTelefono(self):
        return self.__telefono
    def getAltura(self):
        return self.__altura
    def getPeso(self):
        return self.__peso

    def toJSON(self):
        d = dict(
            __class__ = self.__class__.__name__,
            __atributos__ = dict(
                nombre = self.__nombre,
                apellido = self.__apellido,
                telefono = self.__telefono,
                altura = self.__altura,
                peso = self.__peso
            )
        )
        return d

    def reque(self, valor, mensaje):
        if not valor:
            raise ValueError(mensaje)
        return valor