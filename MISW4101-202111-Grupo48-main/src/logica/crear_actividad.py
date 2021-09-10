from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.viajero import ActividadViajero,Viajero
from sqlalchemy import desc
from src.modelo.declarative_base import engine, Base, session


class Crear_Actividad():
    def __init__(self):
        Base.metadata.create_all(engine)

    def validar_limite_caracteres(actividad):
        if len(actividad.nombre) > 255:
            return False
        return True

    def crear_nueva_actividad(nombre):
        actividad = Actividad(nombre=nombre)
        session.add(actividad)
        session.commit()
        session.close()

    def validar_actividad_no_repetida(nombre):
        if(session.query(Actividad).filter(Actividad.nombre == nombre).count() > 0):
            return False
        return True

    def editar_actividad(nombre, actividad):
        actividad.nombre = nombre
        session.commit()

    def eliminar_actividad(actividad):
        if not Crear_Actividad.actividad_tiene_gastos(actividad):
            session.query(Actividad).filter(Actividad.id == actividad.id).delete()
            session.commit()


    def actividad_tiene_gastos(actividad):
        if session.query(Gasto).filter(Gasto.actividad == actividad.id).all():
            return True
        return False
