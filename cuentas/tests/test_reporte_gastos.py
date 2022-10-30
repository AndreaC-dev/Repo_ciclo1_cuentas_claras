import unittest
__author__ = "Andrea Cardenas y Daniel Velasquez"
__copyright__ = "Andrea y Daniel"
__license__ = "mit"
from src.modelo.declarative_base import Session
from src.logica.listado_actividades import Listado_actividades
from faker import Faker
from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero, ActividadViajero
from src.logica.reporte_gastos import Reporte_Gastos
class ReporteGastosTestCase(unittest.TestCase):
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
    def test_generar_matriz_reporte_gastos(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        contador = 0
        valores = 0
        resultado = []
        prueba = []
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
        esperado = [{'Nombre': prueba[0].split()[0], 'Apellido': prueba[0].split()[1], 'Valor': resultado[0]}, {'Nombre': prueba[1].split()[0], 'Apellido': prueba[1].split()[1], 'Valor': resultado[1]}]
        self.assertEqual(Reporte_Gastos.generar_matriz_reporte_gastos(self.actividad), esperado)
        
    def test_reporte_con_viajeros_sin_gastos(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        prueba = []
        for j in range(1, 3):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                                   apellido=self.data_factory.unique.last_name())
            self.session.add(self.viajero)
            self.session.commit()
            prueba.append(self.viajero.nombre + " " + self.viajero.apellido)
            self.session.add(ActividadViajero(actividad_id=self.actividad.id, viajero_id=self.viajero.id))
            self.session.commit()
        esperado = [{'Nombre': prueba[0].split()[0], 'Apellido': prueba[0].split()[1], 'Valor': 0}, {'Nombre': prueba[1].split()[0], 'Apellido': prueba[1].split()[1], 'Valor': 0}]
        self.assertEqual(Reporte_Gastos.reporte_viajeros_sin_gastos(self.actividad), esperado)

    def test_reporte_gastos_sin_viajeros_ni_gastos(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        esperado = []
        self.assertEqual(Reporte_Gastos.generar_matriz_reporte_gastos(self.actividad), esperado)
