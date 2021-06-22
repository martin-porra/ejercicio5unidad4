from vistapaciente import PacientesView, nuevopa, ver

class contrlapacientes:
    def __init__(self,repositorio,vista):
        self.repositorio = repositorio
        self.vista = vista
        self.seleccion = -1
        self.pacientes = list(repositorio.obtenerlistapa())

    def crear(self):
        nuevoPaciente = nuevopa(self.vista).show()
        if nuevoPaciente:
            paciente = self.repositorio.agregar(nuevoPaciente)
            self.pacientes.append(paciente)
            self.vista.agregar(paciente)

    def seleccionar(self, index):
        self.seleccion = index
        paciente = self.pacientes[index]
        self.vista.verpa(paciente)

    def borrapa(self):
        if self.seleccion==-1:
            return
        paciente = self.pacientes[self.seleccion]
        self.repositorio.borrapa(paciente)
        self.pacientes.pop(self.seleccion)
        self.vista.borrapa(self.seleccion)
        self.seleccion=-1

    def ver(self):
        if self.vista.obtenerpa() != None:
            ver(self.vista).show()

    def modificapa(self):
        if self.seleccion==-1:
            return
        rowid = self.pacientes[self.seleccion].rowid
        detallesPaciente = self.vista.obtenerdetalles()
        detallesPaciente.rowid = rowid
        paciente = self.repositorio.modificapa(detallesPaciente)
        self.pacientes[self.seleccion] = paciente
        self.vista.modificapa(paciente, self.seleccion)
        self.seleccion=-1

    def start(self):
        for paciente in self.pacientes:
            self.vista.agregar(paciente)
        self.vista.mainloop()



    def grabar(self):
        self.repositorio.grabarDatos()