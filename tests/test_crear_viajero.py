import unittest
__author__ = "Andrea Cardenas"
__copyright__ = "Andrea"
__license__ = "mit"
from src.logica.crear_viajero import Crear_viajero
from src.modelo.declarative_base import Session
from src.modelo.actividad import Actividad
from src.modelo.viajero import Viajero
from faker import Faker


class CrearviajeroTestCase(unittest.TestCase):
    def setUp(self):
        self.Crear_viajero = Crear_viajero()
        self.session = Session()
        self.data_factory = Faker()

    def tearDown(self):
        self.session = Session()
        busqueda = self.session.query(Viajero).all()
        for viajero in busqueda:
            self.session.delete(viajero)
        self.session.commit()
        self.session.close()

    def test_agregar_viajero(self):
        nombre = self.data_factory.first_name()
        apellido = self.data_factory.last_name()
        self.Crear_viajero.agregar_viajero(nombre, apellido)
        consulta1 = self.session.query(Viajero).filter(Viajero.nombre == nombre, Viajero.apellido == apellido).first()
        self.assertEqual(consulta1.nombre, nombre)
        self.assertEqual(consulta1.apellido, apellido)
        
    def test_agregar_viajero_listo(self):
        nombre = self.data_factory.first_name()
        apellido = self.data_factory.last_name()
        self.assertEqual(self.Crear_viajero.agregar_viajero_listo(nombre, apellido), True)

    def test_agregar_viajero_listo(self):
        nombre = self.data_factory.sentence(200)
        apellido = self.data_factory.last_name()
        self.assertEqual(self.Crear_viajero.agregar_viajero_listo(nombre, apellido), False)

    def test_agregar_viajero_repetido(self):
        nombre = self.data_factory.first_name()
        apellido = self.data_factory.last_name()
        self.Crear_viajero.agregar_viajero(nombre, apellido)
        resultado=self.Crear_viajero.agregar_viajero(nombre, apellido)
        self.assertEqual(resultado, False)

    def test_agregar_solo_texto(self):
        nombre1 = self.data_factory.random_int(1,100)
        apellido1 = self.data_factory.last_name()
        resultado1=self.Crear_viajero.agregar_viajero(nombre1, apellido1)
        nombre2 = self.data_factory.first_name()
        apellido2 = self.data_factory.last_name()
        resultado2=self.Crear_viajero.agregar_viajero(nombre2, apellido2)
        nombre3 = self.data_factory.first_name()
        apellido3 = self.data_factory.date_object()
        resultado3=self.Crear_viajero.agregar_viajero(nombre3, apellido3)
        self.assertEqual(resultado1, False)
        self.assertEqual(resultado2, True)
        self.assertEqual(resultado3, False)

    def test_agregar_datos_completos(self):
        nombre1= ""
        apellido1= self.data_factory.last_name()
        resultado1=self.Crear_viajero.agregar_viajero(nombre1, apellido1)
        nombre2= self.data_factory.first_name()
        apellido2= ""
        resultado2=self.Crear_viajero.agregar_viajero(nombre2, apellido2)
        self.assertEqual(resultado1, False)
        self.assertEqual(resultado2, False)

    def test_limite_caracteres(self):
        nombre = self.data_factory.pystr(min_chars=256, max_chars=300)
        apellido = self.data_factory.pystr(min_chars=256, max_chars=300)
        resultado1=self.Crear_viajero.agregar_viajero(nombre, apellido)
        self.assertEqual(resultado1, False)



