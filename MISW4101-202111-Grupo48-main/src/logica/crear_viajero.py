from src.modelo.declarative_base import engine, Base, session,Session
from src.modelo.viajero import Viajero

class Crear_viajero():
    def __init__(self):
        Base.metadata.create_all(engine)

    def agregar_viajero(self, nombre, apellido):
        busqueda = session.query(Viajero).filter(Viajero.nombre == nombre, Viajero.apellido == apellido).all()
        if len(busqueda) == 0:
            cadena1 = (str(nombre)).isalpha()
            cadena2 = (str(apellido)).isalpha()
            if cadena1 == True and cadena2 == True:
                if len(str(nombre)) < 255 and len(str(apellido)) < 255:
                    self.session = Session()
                    self.viajero = Viajero(nombre=nombre, apellido=apellido)
                    self.session.add(self.viajero)
                    self.session.commit()
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def agregar_viajero_listo(self, nombre, apellido):
        nombre=nombre.capitalize()
        apellido=apellido.capitalize()
        busqueda = session.query(Viajero).filter(Viajero.nombre == nombre, Viajero.apellido == apellido).all()
        if len(busqueda) == 0:
            cadena1 = (str(nombre)).isalpha()
            cadena2 = (str(apellido)).isalpha()
            if cadena1 == True and cadena2 == True:
                if len(str(nombre)) < 255 and len(str(apellido)) < 255:
                    self.session = Session()
                    self.viajero = Viajero(nombre=nombre, apellido=apellido)
                    self.session.add(self.viajero)
                    self.session.commit()
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False





