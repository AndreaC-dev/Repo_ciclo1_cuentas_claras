import unittest
__author__ = "Andrea Cardenas y Daniel Velasquez"
__copyright__ = "Andrea y Daniel"
__license__ = "mit"

from src.modelo.declarative_base import Session
from src.modelo.gasto import Gasto
from src.modelo.actividad import Actividad
from src.modelo.viajero import Viajero
from src.modelo.viajero import ActividadViajero
from src.logica.listado_actividades import Listado_actividades
import datetime
import statistics as stats
from faker import Faker

class ReporteCompensacionesTestCase(unittest.TestCase):
    def setUp(self):
        self.Listado_actividades = Listado_actividades()
        self.session = Session()
        self.data_factory = Faker()

    def tearDown(self):
        self.session = Session()
        busqueda = self.session.query(Actividad).all()
        for actividad in busqueda:
            self.session.delete(actividad)
        busqueda = self.session.query(Viajero).all()
        for viajero in busqueda:
            self.session.delete(viajero)
        self.session.commit()
        self.session.close()

    def test_traer_viajeros_n_viajeros(self):
        viajeros=[]
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        for j in range(1, 3):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                                   apellido=self.data_factory.unique.last_name())
            self.session.add(self.viajero)
            self.session.commit()
            self.session.add(ActividadViajero(actividad_id=self.actividad.id, viajero_id=self.viajero.id))
            self.session.commit()
            viajeros.append(self.viajero.nombre + " " + self.viajero.apellido)
            for k in range(0, 2):
                self.gasto = Gasto(concepto=self.data_factory.unique.word(),
                                    valor=(float(self.data_factory.unique.random_int())),
                                    fecha=self.data_factory.date_object())
                self.session.add(self.gasto)
                self.session.commit()
                self.gasto.actividad = self.actividad.id
                self.gasto.viajero = self.viajero.id
                self.session.commit()
        self.session.commit()
        self.assertEqual(Actividad.traer_n_viajeros(self.actividad), viajeros)

    def test_promediar_gastos(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        contador = 0
        valores=0
        for j in range(1, 3):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                                   apellido=self.data_factory.unique.last_name())
            contador=contador+1
            self.session.add(self.viajero)
            self.session.commit()
            self.session.add(ActividadViajero(actividad_id=self.actividad.id, viajero_id=self.viajero.id))
            self.session.commit()
            for k in range(0, 2):
                self.gasto = Gasto(concepto=self.data_factory.unique.word(),
                                    valor=(float(self.data_factory.unique.random_int())),
                                    fecha=self.data_factory.date_object())
                self.session.add(self.gasto)
                self.session.commit()
                valores=valores+(self.gasto.valor)
                self.gasto.actividad = self.actividad.id
                self.gasto.viajero = self.viajero.id
                self.session.commit()
        self.session.commit()
        promedio=valores/contador
        self.assertEqual(Actividad.promediar_gastos(self.actividad), promedio)

    def test_no_hay_viajeros(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        arreglo = []
        self.assertEqual(Actividad.validar_sin_viajeros(self.actividad), arreglo)

    def test_no_hay_gastos_hay_viajeros(self):
        esperado=[]
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        for j in range(1, 3):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                                   apellido=self.data_factory.unique.last_name())
            self.session.add(self.viajero)
            self.session.commit()
            esperado.append({'viajero': self.viajero.nombre + " " + self.viajero.apellido,'valor': '$0.00'})
            self.session.add(ActividadViajero(actividad_id=self.actividad.id, viajero_id=self.viajero.id))
            self.session.commit()
        self.session.commit()
        self.assertEqual(Actividad.no_hay_gastos_hay_viajeros(self.actividad), esperado)

    def test_sumar_gastos_viajero(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        valores = 0
        self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                               apellido=self.data_factory.unique.last_name())
        self.session.add(self.viajero)
        self.session.commit()
        self.session.add(ActividadViajero(actividad_id=self.actividad.id, viajero_id=self.viajero.id))
        self.session.commit()
        for k in range(0, 3):
            self.gasto = Gasto(concepto=self.data_factory.unique.word(),
                                valor=(float(self.data_factory.unique.random_int())),
                                fecha=self.data_factory.date_object())
            self.session.add(self.gasto)
            self.session.commit()
            valores = valores + (self.gasto.valor)
            self.gasto.actividad = self.actividad.id
            self.gasto.viajero = self.viajero.id
            self.session.commit()
        self.session.commit()
        self.assertEqual(Actividad.sumar_gastos_viajero(self.viajero, self.actividad.id), valores)

    def test_calcular_diferencia(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        contador = 0
        valores=0
        resultado=[]
        for j in range(1, 3):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                                   apellido=self.data_factory.unique.last_name())
            contador=contador+1
            self.session.add(self.viajero)
            self.session.commit()
            self.session.add(ActividadViajero(actividad_id=self.actividad.id, viajero_id=self.viajero.id))
            self.session.commit()
            sumatoria = 0
            for k in range(0, 2):
                self.gasto = Gasto(concepto=self.data_factory.unique.word(),
                                    valor=(float(self.data_factory.unique.random_int())),
                                    fecha=self.data_factory.date_object())
                self.session.add(self.gasto)
                self.session.commit()
                valores=valores+(self.gasto.valor)
                sumatoria=sumatoria+(self.gasto.valor)
                self.gasto.actividad = self.actividad.id
                self.gasto.viajero = self.viajero.id
                self.session.commit()
            resultado.append(sumatoria)
        self.session.commit()
        promedio = valores / contador
        esperado=[promedio -elemento for elemento in resultado]
        self.assertEqual(Actividad.diferencia_gastos(self.actividad), esperado)

    def test_sumar_gastos_encima_promedio(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        contador = 0
        valores=0
        resultado=[]
        for j in range(1, 3):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                                   apellido=self.data_factory.unique.last_name())
            contador=contador+1
            self.session.add(self.viajero)
            self.session.commit()
            self.session.add(ActividadViajero(actividad_id=self.actividad.id, viajero_id=self.viajero.id))
            self.session.commit()
            sumatoria = 0
            for k in range(0, 3):
                self.gasto = Gasto(concepto=self.data_factory.unique.word(),
                                    valor=(float(self.data_factory.unique.random_int())),
                                    fecha=self.data_factory.date_object())
                self.session.add(self.gasto)
                self.session.commit()
                valores=valores+(self.gasto.valor)
                sumatoria=sumatoria+(self.gasto.valor)
                self.gasto.actividad = self.actividad.id
                self.gasto.viajero = self.viajero.id
                self.session.commit()
            resultado.append(sumatoria)
        self.session.commit()
        promedio = valores / contador
        dato=0
        for elemento in resultado:
            if elemento>promedio:
                dato=dato+(elemento-promedio)
        self.assertEqual(Actividad.sumar_gastos_encima_promedio(self.actividad), dato)

    def test_calcular_participacion(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        contador = 0
        valores = 0
        resultado = []
        for j in range(1, 3):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                                   apellido=self.data_factory.unique.last_name())
            contador = contador + 1
            self.session.add(self.viajero)
            self.session.commit()
            self.session.add(ActividadViajero(actividad_id=self.actividad.id, viajero_id=self.viajero.id))
            self.session.commit()
            sumatoria = 0
            for k in range(0, 3):
                self.gasto = Gasto(concepto=self.data_factory.unique.word(),
                                    valor=(float(self.data_factory.unique.random_int())),
                                    fecha=self.data_factory.date_object())
                self.session.add(self.gasto)
                self.session.commit()
                valores = valores + (self.gasto.valor)
                sumatoria = sumatoria + (self.gasto.valor)
                self.gasto.actividad = self.actividad.id
                self.gasto.viajero = self.viajero.id
                self.session.commit()
            resultado.append(sumatoria)
        self.session.commit()
        promedio = valores / contador
        dato = 0
        for elemento in resultado:
            if elemento>promedio:
                dato=dato+(elemento-promedio)
        esperado=[]
        for elemento in resultado:
            if elemento<=promedio:
                esperado.append(0)
            else:
                esperado.append((elemento-promedio)/dato)
        self.assertEqual(Actividad.calcular_participacion(self.actividad), esperado)

    def test_calcular_matriz_2_viajeros(self):

        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        contador = 0
        valores = 0
        resultado = []
        prueba=[]
        for j in range(1, 3):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                                   apellido=self.data_factory.unique.last_name())
            contador = contador + 1
            self.session.add(self.viajero)
            self.session.commit()
            prueba.append(self.viajero.nombre + " " + self.viajero.apellido)
            self.session.add(ActividadViajero(actividad_id=self.actividad.id, viajero_id=self.viajero.id))
            self.session.commit()
            sumatoria = 0
            for k in range(0, 3):
                self.gasto = Gasto(concepto=self.data_factory.unique.word(),
                                    valor=(float(self.data_factory.unique.random_int())),
                                    fecha=self.data_factory.date_object())
                self.session.add(self.gasto)
                self.session.commit()
                valores = valores + (self.gasto.valor)
                sumatoria = sumatoria + (self.gasto.valor)
                self.gasto.actividad = self.actividad.id
                self.gasto.viajero = self.viajero.id
                self.session.commit()
            resultado.append(sumatoria)
        self.session.commit()
        promedio = valores / contador
        dato = 0
        for elemento in resultado:
            if elemento>promedio:
                dato=dato+(elemento-promedio)
        esperado=[]
        contador=0
        lista1=[]
        for elemento in resultado:
            lista1.append(prueba[contador])
            if elemento<=promedio:
                lista1.append((float(format((0), '0.2f'))))
            else:
                lista1.append((float(format(abs((sumatoria-promedio)*((elemento-promedio)/dato)), '0.2f'))))
            contador=contador+1
        contador=1
        for elemento in resultado:
            lista1.insert(contador,-1)
            contador=contador+4
        prueba.insert(0,"")
        esperado.append(prueba)
        esperado.append(lista1[0:3])
        esperado.append(lista1[3:6])
        self.assertEqual(Actividad.calcular_matriz(self.actividad), esperado)

    def test_calcular_matriz_1_viajeros(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        contador = 0
        valores = 0
        resultado = []
        prueba=[]
        for j in range(1):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                                   apellido=self.data_factory.unique.last_name())
            contador = contador + 1
            self.session.add(self.viajero)
            self.session.commit()
            prueba.append(self.viajero.nombre + " " + self.viajero.apellido)
            self.session.add(ActividadViajero(actividad_id=self.actividad.id, viajero_id=self.viajero.id))
            self.session.commit()
            sumatoria = 0
            for k in range(0, 3):
                self.gasto = Gasto(concepto=self.data_factory.unique.word(),
                                    valor=(float(self.data_factory.unique.random_int())),
                                    fecha=self.data_factory.date_object())
                self.session.add(self.gasto)
                self.session.commit()
                valores = valores + (self.gasto.valor)
                sumatoria = sumatoria + (self.gasto.valor)
                self.gasto.actividad = self.actividad.id
                self.gasto.viajero = self.viajero.id
                self.session.commit()
        self.session.commit()
        prueba.insert(0,"")
        resultado.append(self.viajero.nombre + " " + self.viajero.apellido)
        resultado.append(-1)
        esperado=[]
        esperado.append(prueba)
        esperado.append(resultado)
        self.assertEqual(Actividad.calcular_matriz(self.actividad), esperado)
