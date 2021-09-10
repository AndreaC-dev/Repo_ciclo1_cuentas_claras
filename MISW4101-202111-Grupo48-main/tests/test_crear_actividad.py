import unittest

from src.modelo.declarative_base import Session
from src.logica.crear_actividad import Crear_Actividad
from src.logica.listado_actividades import Listado_actividades
from src.modelo.actividad import Actividad
from faker import Faker
from src.modelo.gasto import Gasto
from src.modelo.viajero import ActividadViajero, Viajero



class CrearActividadTestCase(unittest.TestCase):
    def setUp(self):
        self.data_factory = Faker()

    def tearDown(self):
        self.session = Session()
        busqueda = self.session.query(Actividad).all()
        for actividad in busqueda:
            self.session.delete(actividad)
        self.session.commit()

        busqueda = self.session.query(Viajero).all()
        for viajero in busqueda:
            self.session.delete(viajero)
            self.session.commit()
        self.session.close()

    def test_validar_limite_caracteres(self):
        listado_actividades = Listado_actividades()
        self.session = Session()
        Faker.seed(0)
        nombreActividad = self.data_factory.pystr(min_chars=256, max_chars=300)
        actividad_test = Actividad(nombre=nombreActividad)
        self.assertFalse(Crear_Actividad.validar_limite_caracteres(actividad_test))

    def test_validar_actividad_no_repetida(self):
        listado_actividades = Listado_actividades()
        nombreActividad = self.data_factory.unique.word()
        self.session = Session()
        actividadPrueba = Actividad(nombre=nombreActividad)
        self.session.add(actividadPrueba)
        self.session.commit()
        self.session.close()
        self.assertFalse(Crear_Actividad.validar_actividad_no_repetida(nombreActividad))

    def test_crear_actividad(self):
        listado_actividades = Listado_actividades()
        self.session = Session()
        Faker.seed(0)
        nombreActividad = self.data_factory.unique.word()
        contador_actividades = self.session.query(Actividad).count()
        Crear_Actividad.crear_nueva_actividad(nombreActividad)
        self.assertEqual(contador_actividades+1, self.session.query(Actividad).count())

    def test_editar_actividad(self):
        listado_actividades = Listado_actividades()
        nombreActividad = self.data_factory.unique.word()
        self.session = Session()
        actividadPrueba = Actividad(nombre=nombreActividad)
        self.session.add(actividadPrueba)
        self.session.commit()
        self.session.close()
        nuevoNombre = self.data_factory.unique.word()
        Crear_Actividad.editar_actividad(nuevoNombre, actividadPrueba)
        self.assertFalse(actividadPrueba.nombre == nombreActividad)

    def test_eliminar_actividad(self):
        listado_actividades = Listado_actividades()
        nombreActividad = self.data_factory.unique.word() + '' + self.data_factory.unique.word()
        self.session = Session()
        actividadPrueba = Actividad(nombre=nombreActividad)
        self.session.add(actividadPrueba)
        self.session.commit()
        Crear_Actividad.eliminar_actividad(actividadPrueba)
        self.assertTrue(self.session.query(Actividad).filter(Actividad.nombre == nombreActividad).count() == 0)

    def test_eliminar_actividad_con_gastos(self):
        listado_actividades = Listado_actividades()
        self.session = Session()
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
        Crear_Actividad.eliminar_actividad(self.actividad)
        num = self.session.query(Actividad).filter(Actividad.nombre == self.actividad.nombre).count()
        self.assertFalse(num == 0)
