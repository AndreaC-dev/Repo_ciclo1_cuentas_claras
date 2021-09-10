from src.modelo.declarative_base import engine, Base, session
from src.modelo.gasto import Gasto
from src.modelo.viajero import ActividadViajero,Viajero
from sqlalchemy import desc, func

class Reporte_Gastos():

    def __init__(self):
        Base.metadata.create_all(engine)

    def generar_matriz_reporte_gastos(actividad):
        gastos = session.query(Gasto.viajero, func.sum(Gasto.valor).label("valor")).filter(Gasto.actividad == actividad.id).group_by(Gasto.viajero).all()
        gastos_consolidados = []
        cantidad_viajeros = session.query(ActividadViajero).filter(ActividadViajero.actividad_id == actividad.id).count()
        if cantidad_viajeros > 0 and not gastos:
            return Reporte_Gastos.reporte_viajeros_sin_gastos(actividad)
        for gasto in gastos:
            viajero = session.query(Viajero).filter(Viajero.id == gasto.viajero).first()
            nombre = viajero.nombre
            apellido = viajero.apellido
            gastos_consolidados.append({"Nombre": nombre, "Apellido": apellido, "Valor": gasto.valor})
        return gastos_consolidados

    def reporte_viajeros_sin_gastos(actividad):
        viajeros_id = session.query(ActividadViajero).filter(ActividadViajero.actividad_id == actividad.id).all()
        reporte_gastos = []
        for id in viajeros_id:
            viajero = session.query(Viajero).filter(Viajero.id == id.viajero_id).first()
            nombre = viajero.nombre
            apellido = viajero.apellido
            reporte_gastos.append({"Nombre": nombre, "Apellido": apellido, "Valor": 0})
        return reporte_gastos
