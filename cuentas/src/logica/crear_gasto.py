from src.modelo.declarative_base import engine, Base, session,Session
from src.modelo.viajero import Viajero
from src.modelo.gasto import Gasto
from src.modelo.viajero import ActividadViajero
from sqlalchemy import and_


class Crear_gasto():
    def __init__(self):
        Base.metadata.create_all(engine)

    def mostrar_nombre_viajeros(self):
        busqueda = session.query(Viajero).all()
        resultado = []
        for viajero in busqueda:
            resultado.append({"Nombre": viajero.nombre, "Apellido": viajero.apellido})
        return resultado

    def mostrar_nombre_viajeros_ordenado(self):
        busqueda = session.query(Viajero).all()
        lista = sorted(busqueda, key=lambda x: (x.apellido, x.nombre))
        resultado = []
        for viajero in lista:
            resultado.append({"Nombre": viajero.nombre, "Apellido": viajero.apellido})
        return resultado

    def mostrar_nombre_viajeros_actividad(self):
        id_viajeros = [r.viajero_id for r in session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == self.id)]
        viajeros = session.query(Viajero).all()
        resultado = []
        for viajero in viajeros:
            if viajero.id in id_viajeros:
                resultado.append({"Nombre": viajero.nombre, "Apellido": viajero.apellido})
        return resultado

    def hallar_viajero(self):
        busqueda = session.query(Viajero).all()
        resultado = []
        persona=[self]
        for viajero in busqueda:
                resultado.append(viajero.id)
                resultado.append([viajero.nombre + " " + viajero.apellido])
        dato2 = resultado.index(persona)
        id=resultado[(dato2-1)]
        return id

    def crear_gasto(self, actividad,concepto,fecha,valor,viajero):
        id=Crear_gasto.hallar_viajero(viajero)
        cadena=str(type(valor))
        if cadena == '<class \'float\'>' or cadena == '<class \'int\'>':
            if len(str(concepto)) > 0 and len(str(valor)) > 0:
                if len(str(concepto)) < 255 and len(str(valor)) < 255:
                    self.session = Session()
                    self.gasto = Gasto(concepto=concepto, valor=valor, fecha=fecha, actividad=actividad, viajero=id)
                    self.session.add(self.gasto)
                    self.session.commit()
                    self.session.close()
                    return True
                return False
            return False
        return False

    def crear_gasto_listo(self, concepto,fecha,valor,viajero):
        numero=self.id
        id = Crear_gasto.hallar_viajero(viajero)
        try:
            float(valor)
            cadena= True
        except ValueError:
            cadena= False
        if cadena == True:
            if len(str(concepto)) >0 and len(str(valor)) >0:
                if len(str(concepto)) < 255 and len(str(valor)) <255:
                    session = Session()
                    dato=fecha.toPyDate()
                    gasto = Gasto(concepto=concepto, valor=(valor), fecha=dato,actividad=numero,viajero=id)
                    session.add(gasto)
                    session.commit()
                    return True
                return False
            return False
        return False

    def mostrar_nombre_viajeros_actividad_ordenado(self):
        id_viajeros = [r.viajero_id for r in session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == self.id)]
        viajeros = session.query(Viajero).all()
        lista = sorted(viajeros, key=lambda x: (x.apellido, x.nombre))
        resultado = []
        for viajero in lista:
            if viajero.id in id_viajeros:
                resultado.append({"Nombre": viajero.nombre, "Apellido": viajero.apellido})
        return resultado

    def poblar_viajero(self,actividad):
        id=self
        busqueda=session.query(Gasto).filter(Gasto.id==id).first()
        tabla=[]
        id_viajero=busqueda.viajero
        viajero = session.query(Viajero).filter(Viajero.id==id_viajero).first()
        tabla=({"Nombre":viajero.nombre,"Apellido":viajero.apellido})
        return tabla

    def editar_gasto(actividad, gasto, concepto, fecha, valor, viajero):
        id = Crear_gasto.hallar_viajero(viajero)
        cadena = str(type(valor))
        if cadena == '<class \'float\'>' or cadena == '<class \'int\'>':
            if len(str(concepto)) > 0 and len(str(valor)) > 0:
                if len(str(concepto)) < 255 and len(str(valor)) < 255:
                    session = Session()
                    session.query(Gasto).filter(Gasto.id == gasto).update(
                        {"concepto": concepto, "valor": valor, "fecha": fecha,
                         "viajero": id})
                    session.commit()
                    gasto = session.query(Gasto).filter(Gasto.id == gasto).first()
                    return gasto
                return False
            return False
        return False

    def editar_gasto_listo(actividad, gasto, concepto, fecha, valor, viajero):
        id = Crear_gasto.hallar_viajero(viajero)
        try:
            float(valor)
            cadena = True
        except ValueError:
            cadena = False
        if cadena == True:
            if len(str(concepto)) > 0 and len(str(valor)) > 0:
                if len(str(concepto)) < 255 and len(str(valor)) < 255:
                    session = Session()
                    dato = fecha.toPyDate()
                    session.query(Gasto).filter(Gasto.id == gasto.id).update(
                        {"concepto": concepto, "valor": valor, "fecha": dato,
                         "viajero": id})
                    session.commit()
                    gasto.concepto = concepto
                    gasto.valor = float(valor)
                    gasto.fecha = dato
                    gasto.viajero = id
                    return True
                return False
            return False
        return False
