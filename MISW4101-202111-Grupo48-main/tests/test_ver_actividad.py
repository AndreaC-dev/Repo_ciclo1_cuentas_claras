import unittest

from src.modelo.declarative_base import Session
from src.modelo.gasto import Gasto
from src.logica.ver_actividad import Ver_actividad
from src.modelo.actividad import Actividad
from src.modelo.viajero import Viajero
from src.modelo.viajero import ActividadViajero
import datetime
from faker import Faker



class VerActividadTestCase(unittest.TestCase):

    def setUp(self):
        self.ver_actividad = Ver_actividad()
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


    def test_validar_actividad_sin_gastos(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        self.assertEqual(Ver_actividad.validar_gastos_de_actividades(self.actividad),0)

    def test_validar_actividad_un_gasto(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        self.gasto = Gasto(concepto=self.data_factory.unique.word(), valor=(float(self.data_factory.unique.random_int())),
                       fecha=self.data_factory.date_object())
        self.session.add(self.gasto)
        self.session.commit()
        self.gasto.actividad = self.actividad.id
        self.session.commit()
        self.assertEqual(Ver_actividad.validar_gastos_de_actividades(self.actividad), 1)

    def test_validar_actividad_n_gastos(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        for i in range(0, 2):
            self.gasto = Gasto(concepto=self.data_factory.unique.word(), valor=(float(self.data_factory.unique.random_int())),
                           fecha=self.data_factory.date_object())
            self.session.add(self.gasto)
            self.session.commit()
            self.gasto.actividad = self.actividad.id
        self.session.commit()
        self.assertEqual(Ver_actividad.validar_gastos_de_actividades(self.actividad), 2)

    def test_mostrar_nombre_viajero(self):
        viajeros =[]
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
            viajeros.append(self.viajero.nombre + " "+self.viajero.apellido)
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
        self.assertEqual(Ver_actividad.mostrar_nombre_viajeros(self.actividad), viajeros)

    def test_ordenar_por_fecha(self):
        fechas=[]
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        for i in range(0, 3):
            self.gasto = Gasto(concepto=self.data_factory.unique.word(),
                                valor=(float(self.data_factory.unique.random_int())),
                                fecha=self.data_factory.date_object())
            self.session.add(self.gasto)
            self.session.commit()
            fechas.append(self.gasto.fecha)
            self.gasto.actividad = self.actividad.id
        self.session.commit()
        ordenado=(sorted(fechas,reverse=True))
        self.assertEqual(Ver_actividad.ordenar_gastos_por_fecha(self.actividad), ordenado)

    def test_formato_fecha(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        self.gasto = Gasto(concepto=self.data_factory.unique.word(), valor=(float(self.data_factory.unique.random_int())),
                       fecha=self.data_factory.date_object())
        self.session.add(self.gasto)
        self.session.commit()
        self.gasto.actividad = self.actividad.id
        self.session.commit()
        formato = self.gasto.fecha.strftime('%d/%m/%Y')
        self.assertEqual(Ver_actividad.mostrar_formato_fecha(self.actividad), formato)

    def test_formato_valor(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        self.gasto = Gasto(concepto=self.data_factory.unique.word(), valor=(float(self.data_factory.unique.random_int())),
                       fecha=self.data_factory.date_object())
        self.session.add(self.gasto)
        self.session.commit()
        self.gasto.actividad = self.actividad.id
        self.session.commit()
        formato = str("$" + format(self.gasto.valor, '0.2f'))
        self.assertEqual(Ver_actividad.formato_valor(self.actividad), formato)

    def test_mostrar_conceptos(self):
        conceptos = []
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        for i in range(0, 3):
            self.gasto = Gasto(concepto=self.data_factory.unique.word(),
                                valor=(float(self.data_factory.unique.random_int())),
                                fecha=self.data_factory.date_object())
            self.session.add(self.gasto)
            self.session.commit()
            conceptos.append(self.gasto.concepto)
            self.gasto.actividad = self.actividad.id
        self.session.commit()
        self.assertEqual(Ver_actividad.mostrar_concepto(self.actividad), conceptos)

    def test_mostrar_fechas(self):
        fechas = []
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        for i in range(0, 3):
            self.gasto = Gasto(concepto=self.data_factory.unique.word(),
                                valor=(float(self.data_factory.unique.random_int())),
                                fecha=self.data_factory.date_object())
            self.session.add(self.gasto)
            self.session.commit()
            fechas.append(self.gasto.fecha)
            self.gasto.actividad = self.actividad.id
        self.session.commit()
        self.assertEqual(Ver_actividad.mostrar_fechas(self.actividad), fechas)

    def test_mostrar_valores(self):
        valores = []
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        for i in range(0, 3):
            self.gasto = Gasto(concepto=self.data_factory.unique.word(),
                                valor=(float(self.data_factory.unique.random_int())),
                                fecha=self.data_factory.date_object())
            self.session.add(self.gasto)
            self.session.commit()
            valores.append(self.gasto.valor)
            self.gasto.actividad = self.actividad.id
        self.session.commit()
        self.assertEqual(Ver_actividad.mostrar_valores(self.actividad), valores)