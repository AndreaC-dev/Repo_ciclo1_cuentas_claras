from src.modelo.declarative_base import engine, Base, session,Session
from src.modelo.actividad import Actividad
from src.modelo.viajero import Viajero
from src.modelo.viajero import ActividadViajero,Viajero


class Listado_actividades():
    def __init__(self):
        Base.metadata.create_all(engine)

    def mostrar_actividades(self):
        actividades = session.query(Actividad).all()
        return actividades

    def mostrar_nombres_actividades(self):
        actividades=session.query(Actividad).all()
        resultado=[]
        for actividad in actividades:
            resultado.append(actividad.nombre)
        return resultado

    def validar_almacenamiento(self):
        busqueda = session.query(Actividad.nombre).filter(Actividad.nombre == self).all()
        return busqueda

    def ordenar_lista_actividades(lista_actividades):
        if not lista_actividades:
            return []
        return sorted(lista_actividades, key=lambda x: x.nombre)

    def ordenar_lista_nombre_actividades(lista_actividades):
        return sorted(lista_actividades)

    def mostrar_nombre_viajeros(self):
        busqueda = session.query(Viajero).all()
        resultado=[]
        for viajero in busqueda:
            lista=(viajero.nombre+" "+viajero.apellido)
            resultado.append(lista)
        return resultado

    def ordenar_lista_nombre_viajeros(lista_viajeros):
        if not lista_viajeros:
            return []
        return sorted(lista_viajeros, key=lambda x:(x.apellido, x.nombre))

    def mostrar_si_viajeros_pertenecen_desorden(self):
        id_viajeros = [r.viajero_id for r in
                       session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == self)]
        busqueda = session.query(Viajero).all()
        resultado = []
        for viajero in busqueda:
            if viajero.id in id_viajeros:
                resultado.append({"Nombre": viajero.nombre + " " + viajero.apellido, "Presente": True})
            else:
                resultado.append({"Nombre": viajero.nombre + " " + viajero.apellido, "Presente": False})
        return resultado

    def mostrar_si_viajeros_pertenecen(self):
        id_viajeros = [r.viajero_id for r in
                       session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == self)]
        busqueda = session.query(Viajero).all()
        lista=sorted(busqueda, key=lambda x:(x.apellido, x.nombre))
        resultado = []
        for viajero in lista:
            if viajero.id in id_viajeros:
                resultado.append({"Nombre": viajero.nombre + " " + viajero.apellido,"Presente": True})
            else:
                resultado.append({"Nombre": viajero.nombre + " " + viajero.apellido,"Presente": False})
        return resultado

    def agregar_viajero_con_check(self,viajeros,actividad):
        id_viajeros = [r.viajero_id for r in
                       session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == actividad)]
        busqueda = session.query(Viajero).all()
        resultado = []
        for viajero in busqueda:
                resultado.append(viajero.id)
                resultado.append([viajero.nombre + " " + viajero.apellido])
        dato=[]
        for viajero in viajeros:
            if viajero["Presente"]:
                dato.append(viajero["Nombre"])
                dato2 = resultado.index(dato)
                id=resultado[(dato2-1)]
                dato=[]
                if not id in id_viajeros:
                    self.session = Session()
                    self.session.add(ActividadViajero(actividad_id=actividad, viajero_id=id))
                    self.session.commit()
                    self.session.close()
        for viajero in viajeros:
            if not viajero["Presente"]:
                dato.append(viajero["Nombre"])
                dato2 = resultado.index(dato)
                id=resultado[(dato2-1)]
                dato=[]
                if id in id_viajeros:
                    self.session = Session()
                    self.session.query(ActividadViajero).filter(ActividadViajero.actividad_id == actividad,
                                                                ActividadViajero.viajero_id == id).delete()
                    self.session.commit()
                    self.session.close()

    def agregar_viajero_check(self, viajeros):
        session = Session()
        id_viajeros = [r.viajero_id for r in
                       session.query(ActividadViajero.viajero_id).filter(
                           ActividadViajero.actividad_id == self)]
        busqueda = session.query(Viajero).all()
        resultado = []
        for viajero in busqueda:
            resultado.append(viajero.id)
            resultado.append([viajero.nombre + " " + viajero.apellido])
        dato = []
        for viajero in viajeros:
            if viajero["Presente"]:
                dato.append(viajero["Nombre"])
                dato2 = resultado.index(dato)
                id = resultado[(dato2 - 1)]
                dato = []
                if not id in id_viajeros:
                    session = Session()
                    session.add(ActividadViajero(actividad_id=self, viajero_id=id))
                    session.commit()
                    session.close()
        for viajero in viajeros:
            if not viajero["Presente"]:
                dato.append(viajero["Nombre"])
                dato2 = resultado.index(dato)
                id = resultado[(dato2 - 1)]
                dato = []
                if id in id_viajeros:
                    session = Session()
                    session.query(ActividadViajero).filter(ActividadViajero.actividad_id == self,
                                                                ActividadViajero.viajero_id == id).delete()
                    session.commit()
                    session.close()
        id_viajeros = [r.viajero_id for r in
                       session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == self)]
        busqueda = session.query(Viajero).all()
        resultado = []
        for viajero in busqueda:
            if viajero.id in id_viajeros:
                resultado.append({"Nombre": viajero.nombre + " " + viajero.apellido, "Presente": True})
            else:
                resultado.append({"Nombre": viajero.nombre + " " + viajero.apellido, "Presente": False})
        return resultado




