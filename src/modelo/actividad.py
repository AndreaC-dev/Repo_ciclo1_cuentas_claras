from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.modelo.viajero import ActividadViajero
from src.modelo.viajero import Viajero
from src.modelo.declarative_base import Base, session
from src.modelo.gasto import Gasto

class Actividad(Base):
    __tablename__ = 'actividad'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    viajeros = relationship('Viajero', secondary='actividad_viajero')
    gastos = relationship('Gasto', cascade='all, delete, delete-orphan')

    def promediar_gastos(self):

        query = session.query(Gasto).filter(Gasto.actividad == self.id).all()
        sumatoria = 0
        for gastos in query:
            sumatoria =sumatoria+gastos.valor

        cantidad = session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == self.id).count()
        promedio = sumatoria / cantidad
        return promedio

    def traer_n_viajeros(self):
        id_viajeros = [r.viajero_id for r in session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == self.id)]
        viajeros = session.query(Viajero).all()
        resultado = []
        for viajero in viajeros:
            if viajero.id in id_viajeros:
                resultado.append(viajero.nombre+" "+viajero.apellido)

        return resultado

    def validar_sin_viajeros(self):
        viajeros_actividad = session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == self.id).all()
        if len(viajeros_actividad) == 0:
            return []
        return viajeros_actividad

    def no_hay_gastos_hay_viajeros(self):
        viajeros_actividad = session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == self.id).all()
        if len(viajeros_actividad) > 0:
            query = session.query(Gasto).filter(Gasto.actividad == self.id).count()
            if query == 0:
                id_viajeros = [r.viajero_id for r in session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == self.id)]
                viajeros = session.query(Viajero).all()
                matriz = []

                for viajero in viajeros:
                    if viajero.id in id_viajeros:
                        matriz.append({'viajero' : viajero.nombre + " " + viajero.apellido,'valor' : '$0.00'})
        return matriz

    def sumar_gastos_viajero(self, idActividad):
        gastos_viajero = session.query(Gasto).filter(Gasto.viajero == self.id, Gasto.actividad == idActividad).all()
        lista_gastos_viajero = []
        for gasto in gastos_viajero:
            lista_gastos_viajero.append(gasto.valor)
        sumatoria_gastos_viajero = sum(lista_gastos_viajero)
        return sumatoria_gastos_viajero

    def diferencia_gastos(self):
        id_viajeros = [viajero.viajero_id for viajero in
                       session.query(ActividadViajero.viajero_id).filter(ActividadViajero.actividad_id == self.id)]
        viajeros = session.query(Viajero).all()
        resultado = []
        for viajero in viajeros:
            if viajero.id in id_viajeros:
                gastos_viajero = Actividad.sumar_gastos_viajero(viajero, self.id)
                promedio = self.promediar_gastos()
                diferencia = promedio - gastos_viajero
                resultado.append(diferencia)

        return resultado

    def sumar_gastos_encima_promedio(self):
        sumatoria_gastos_encima_promedio = self.diferencia_gastos()
        diferencia_gastos = sum(e for e in sumatoria_gastos_encima_promedio if e >= 0)
        return diferencia_gastos

    def calcular_participacion(self):
        diferencia = self.diferencia_gastos()
        lista=(list(diferencia))
        suma = self.sumar_gastos_encima_promedio()
        resultado=[]
        for lista in lista:
            if lista < 0:
                resultado.append(float(((lista / suma))))
            else:
                resultado.append(0)
        resultado= [abs(ele) for ele in resultado]
        return resultado

    def calcular_matriz(self):
        diferencia = self.diferencia_gastos()
        lista=(list(diferencia))
        participacion = self.calcular_participacion()
        id_viajeros = [r.viajero_id for r in session.query(ActividadViajero.viajero_id).filter(
            ActividadViajero.actividad_id == self.id)]
        viajeros = session.query(Viajero).all()
        numero=(len(lista))+1
        resultado = []
        el = []
        n=0
        for a in participacion:
            for b in lista:
                multiply = a * b
                for i in range(1):
                    if multiply > 0:
                        el.insert(n, (float(format((multiply), '0.2f'))))
                    else:
                        el.insert(n, (float(format((0), '0.2f'))))
                    n=n+1
            n=n+numero
        n=0
        for viajero in viajeros:
            if viajero.id in id_viajeros:
                x = viajero.nombre + " " + viajero.apellido
                el.insert(n,x)
                n=n+numero
        n=1
        for viajero in viajeros:
            if viajero.id in id_viajeros:
                el[n]=-1
                n=n+numero+1
        n=0
        fila1=[]
        for viajero in viajeros:
            if viajero.id in id_viajeros:
                fila1.append(viajero.nombre + " " + viajero.apellido)
                n=n+1
        fila1.insert(0,'')
        y=len(fila1)
        x = len(el)
        resultado.append(fila1)
        for i in range(0,x,y):
            resultado.append(el[i:i+y])
        return resultado




