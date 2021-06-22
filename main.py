from claserepositoriopaciente import repositoriopaciente
from vistapaciente import PacientesView
from clascontroladorpaciente import contrlapacientes
from claseobject import ObjectEncoder


def main():
    enco=ObjectEncoder('paciente.json')
    repositorio=repositoriopaciente(enco)
    vista=PacientesView()
    ctrl=contrlapacientes(repositorio, vista)
    vista.setControlador(ctrl)
    ctrl.start()
    ctrl.grabar()

if __name__ == "__main__":
    main()