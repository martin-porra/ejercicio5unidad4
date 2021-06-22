import tkinter as tk
from tkinter import StringVar, messagebox
from tkinter.constants import E, N, S, W
from clasepaciente import Paciente

class listarpacientes(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master)
        self.lb = tk.Listbox(self, **kwargs)
        scroll = tk.Scrollbar(self, command=self.lb.yview)
        self.lb.config(yscrollcommand=scroll.set)
        scroll.grid(column=1,row=0, sticky=(N,S))
        self.lb.grid(column=0, row=0)

    def insertar(self, contacto, index=tk.END):
        text = "{}, {}".format(contacto.getApellido(), contacto.getNombre())
        self.lb.insert(index, text)
    def borrar(self, index):
        self.lb.delete(index, index)
    def modificar(self, contact, index):
        self.borrar(index)
        self.insertar(contact, index)
    def bind_doble_click(self, callback):
        handler = lambda _: callback(self.lb.curselection()[0])
        self.lb.bind("<Double-Button-1>", handler)


class PacienteForm(tk.LabelFrame):
    fields = ("Apellido", "Nombre","Telefono", "Altura", "Peso")
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Paciente", padx=10, pady=10, **kwargs)
        self.frame = tk.Frame(self)
        self.entries = list(map(self.crearCampo, enumerate(self.fields)))
        self.frame.grid(columnspan=3)

    def crearCampo(self, field):
        position, text = field
        label = tk.Label(self.frame, text=text)
        entry = tk.Entry(self.frame, width=30)
        label.grid(row=position, column=0, pady=(5,10), sticky=W)
        entry.grid(row=position, column=1, pady=5)
        return entry

    def mostrarEstadoPacienteEnFormulario(self, paciente):
        values = (paciente.getApellido(), paciente.getNombre(),
                  paciente.getTelefono(), paciente.getAltura(),
                  paciente.getPeso())
        for entry, value in zip(self.entries, values):
            entry.delete(0, tk.END)
            entry.insert(0, value)

    def crearDesdeFormulario(self):
        values = [e.get() for e in self.entries]
        paciente=None
        try:
            paciente = Paciente(*values)
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e), parent=self)
        return paciente

    def obtenerpaDesdeFormulario(self):
        values = [e.get() for e in self.entries]
        paciente = None
        if '' in values:
            messagebox.showwarning("Advertencia",'Seleccione un paciente para ver su IMC', parent=self)
        else:
            paciente = Paciente(*values)
        return paciente

    def limpiar(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

class nuevopa(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.title('Nuevo paciente')
        self.resizable(0,0)
        self.paciente = None
        self.form = PacienteForm(self)
        self.btn_add = tk.Button(self,text="Confirmar",command=self.confirmar)
        self.form.grid(column=0, row = 0, sticky=(W,E), padx=(10,10),pady=(10,10))
        self.btn_add.grid(column=0, row = 1, pady=(0,10))

    def confirmar(self):
        self.paciente = self.form.crearDesdeFormulario()
        if self.paciente:
            self.destroy()

    def show(self):
        self.grab_set()
        self.wait_window()
        return self.paciente

class ver(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.title("IMC")
        self.resizable(0,0)
        self.imc = StringVar()
        self.composicion = StringVar()
        self.paciente = parent.obtenerpa()
        self.calcularIMC()

        self.form = tk.Frame(self)
        self.lbl_imc = tk.Label(self.form,text="IMC [kg/m2]")
        self.lbl_comp = tk.Label(self.form,text="Composición Corporal")
        self.btn_add = tk.Button(self,text="Volver", command=self.volver) #agregar funcionalidad
        self.imcEntry = tk.Entry(self.form,textvariable=self.imc,width=25)
        self.composicionEntry = tk.Entry(self.form,textvariable=self.composicion, width=25)

        self.form.grid(column=0, row = 0, sticky=(W,E), padx=(10,10),pady=(10,10))
        self.lbl_imc.grid(column=0, row=0)
        self.lbl_comp.grid(column=0,row=1)
        self.imcEntry.grid(column=1,row=0)
        self.composicionEntry.grid(column=1,row=1)

        self.btn_add.grid(column=0, row = 1, pady=(0,10))

    def calcularIMC(self):
        altura = float(self.paciente.getAltura()) / 100
        peso = float(self.paciente.getPeso())
        imc = peso / altura**2
        imc = round(imc,2)
        if imc < 18.5:
            composicion = "Peso inferior al normal"
        elif imc >= 18.5 and imc < 25:
            composicion = "Peso normal"
        elif imc >= 25 and imc < 30:
            composicion = "Peso superior al normal"
        else:
            composicion = "Obesidad"
        self.imc.set(str(imc))
        self.composicion.set(composicion)

    def show(self):
        self.grab_set()
        self.wait_window()
        return self.paciente

    def volver(self):
        self.destroy()

class actualizarpaForm(PacienteForm):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.btn_imc = tk.Button(self, text="Ver IMC", command=self.showIMC)
        self.btn_save = tk.Button(self, text="Guardar")
        self.btn_delete = tk.Button(self, text="Borrar")

        self.btn_imc.grid(column=0,row = 8, pady=(5,5))
        self.btn_save.grid(column=1,row=8,pady=(5,5))
        self.btn_delete.grid(column=2,row=8,pady=(5,5))

    def bind_save(self, callback):
        self.btn_save.config(command=callback)
    def bind_delete(self, callback):
        self.btn_delete.config(command=callback)
    def showIMC(self, callback): #Recibe la funcion de ver imc del controlador para que se ejecute al presionar el boton
        self.btn_imc.config(command=callback)


class PacientesView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lista de Pacientes")
        self.resizable(0,0)
        self.list = listarpacientes(self, height=15)
        self.form = actualizarpaForm(self)
        self.btn_new = tk.Button(self, text="Agregar Paciente")

        self.list.grid(column=0,row=0, pady=(10,0), padx=(10,10))
        self.form.grid(column=1,row=0, pady=(5,0), padx=(10,10), sticky=N)
        self.btn_new.grid(column=1,row=1, pady=(10,10))

    def setControlador(self, ctrl):
        self.btn_new.config(command=ctrl.crear)
        self.list.bind_doble_click(ctrl.seleccionar)
        self.form.bind_save(ctrl.modificapa)
        self.form.bind_delete(ctrl.borrapa)
        self.form.showIMC(ctrl.ver)

    def agregar(self, paciente):
        self.list.insertar( paciente)
    def modificapa(self,  paciente, index):
        self.list.modificar( paciente, index)
    def borrapa(self, index):
        self.form.limpiar()
        self.list.borrar(index)


    def obtenerdetalles(self):
        return self.form.crearDesdeFormulario()

    def obtenerpa(self):
        return self.form.obtenerpaDesdeFormulario()


    def verpa(self, contacto):
        self.form.mostrarEstadoPacienteEnFormulario(contacto)