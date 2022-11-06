import unittest
__author__ = "Andrea Cardenas"
__copyright__ = "Andrea"
__license__ = "mit"
from src.logica.crear_viajero import Crear_viajero
from src.modelo.declarative_base import Session,session
from src.modelo.actividad import Actividad
from src.modelo.viajero import Viajero
from src.modelo.gasto import Gasto
from faker import Faker
from src.logica.crear_gasto import Crear_gasto
from src.modelo.viajero import ActividadViajero


class CrearviajeroTestCase(unittest.TestCase):
    def setUp(self):
        self.Crear_gasto = Crear_gasto()
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
        busqueda = self.session.query(Gasto).all()
        for gasto in busqueda:
            self.session.delete(gasto)
        self.session.commit()
        self.session.close()

    def test_traer_todos_los_viajeros(self):
        viajeros=[]
        for i in range(1, 5):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                              apellido=self.data_factory.unique.last_name())
            self.session.add(self.viajero)
            self.session.commit()
            viajeros.append({"Nombre": self.viajero.nombre, "Apellido": self.viajero.apellido})
        self.assertEqual(Crear_gasto.mostrar_nombre_viajeros(self), viajeros)

    def test_hallar_viajero(self):
        for i in range(1, 5):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                              apellido=self.data_factory.unique.last_name())
            self.session.add(self.viajero)
            self.session.commit()
        persona=(self.viajero.nombre+" "+self.viajero.apellido)
        self.assertEqual(Crear_gasto.hallar_viajero(persona), 4)

    def test_crear_gasto(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                               apellido=self.data_factory.unique.last_name())
        persona = (self.viajero.nombre+" "+self.viajero.apellido)
        self.session.add(self.viajero)
        self.session.commit()
        concepto=self.data_factory.unique.word()
        valor = (float(self.data_factory.unique.random_int()))
        fecha = self.data_factory.date_object()
        actividad=self.actividad.id
        self.Crear_gasto.crear_gasto(actividad,concepto,fecha,valor,persona)
        consulta1=self.session.query(Gasto).filter(Gasto.concepto == concepto, Gasto.actividad == actividad, Gasto.viajero == self.viajero.id).first()
        self.assertEqual(consulta1.concepto, concepto)
        self.assertEqual(consulta1.actividad, actividad)
        self.assertEqual(consulta1.viajero, self.viajero.id)

    def test_traer_viajeros_n_viajeros(self):
        viajeros=[]
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        for j in range(1, 5):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                                   apellido=self.data_factory.unique.last_name())
            self.session.add(self.viajero)
            self.session.commit()
            self.session.add(ActividadViajero(actividad_id=self.actividad.id, viajero_id=self.viajero.id))
            self.session.commit()
            viajeros.append({"Nombre": self.viajero.nombre, "Apellido": self.viajero.apellido})
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
        self.assertEqual(Crear_gasto.mostrar_nombre_viajeros_actividad(self.actividad), viajeros)

    def test_no_crear_vacios(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                               apellido=self.data_factory.unique.last_name())
        persona = (self.viajero.nombre+" "+self.viajero.apellido)
        self.session.add(self.viajero)
        self.session.commit()
        concepto=""
        valor = ""
        fecha = self.data_factory.date_object()
        actividad=self.actividad.id
        consulta1=self.Crear_gasto.crear_gasto(actividad,concepto,fecha,valor,persona)
        self.assertEqual(consulta1, False)

    def test_limite_caracteres(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                               apellido=self.data_factory.unique.last_name())
        persona = (self.viajero.nombre+" "+self.viajero.apellido)
        self.session.add(self.viajero)
        self.session.commit()
        concepto = self.data_factory.pystr(min_chars=256, max_chars=300)
        valor = (float(self.data_factory.unique.random_int()))
        fecha = self.data_factory.date_object()
        actividad=self.actividad.id
        consulta1=self.Crear_gasto.crear_gasto(actividad,concepto,fecha,valor,persona)
        self.assertEqual(consulta1, False)

    def test_valor_numerico(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                               apellido=self.data_factory.unique.last_name())
        persona = (self.viajero.nombre+" "+self.viajero.apellido)
        self.session.add(self.viajero)
        self.session.commit()
        concepto1 = self.data_factory.unique.word()
        valor1 = (self.data_factory.unique.random_int())
        fecha1 = self.data_factory.date_object()
        actividad=self.actividad.id
        valor2 = self.data_factory.unique.word()
        valor3 = self.data_factory.date_object()
        valor4 = (float(self.data_factory.unique.random_int()))
        valor5 = self.data_factory.boolean()
        consulta1=self.Crear_gasto.crear_gasto(actividad,concepto1,fecha1,valor1,persona)
        consulta2=self.Crear_gasto.crear_gasto(actividad,concepto1,fecha1,valor2,persona)
        consulta3=self.Crear_gasto.crear_gasto(actividad,concepto1,fecha1,valor3,persona)
        consulta4=self.Crear_gasto.crear_gasto(actividad,concepto1,fecha1,valor4,persona)
        consulta5=self.Crear_gasto.crear_gasto(actividad,concepto1,fecha1,valor5,persona)
        self.assertEqual(consulta1, True)
        self.assertEqual(consulta2, False)
        self.assertEqual(consulta3, False)
        self.assertEqual(consulta4, True)
        self.assertEqual(consulta5, False)

    def test_poblar_viajero(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        for i in range(1, 4):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                                   apellido=self.data_factory.unique.last_name())
            self.session.add(self.viajero)
            self.session.commit()
            self.session.add(ActividadViajero(actividad_id=self.actividad.id, viajero_id=self.viajero.id))
            self.session.commit()

        self.viajero1 = Viajero(nombre=self.data_factory.unique.first_name(),
                               apellido=self.data_factory.unique.last_name())
        self.session.add(self.viajero1)
        self.session.commit()
        self.session.add(ActividadViajero(actividad_id=self.actividad.id, viajero_id=self.viajero1.id))
        self.session.commit()
        self.gasto = Gasto(concepto=self.data_factory.unique.word(),
                           valor=(float(self.data_factory.unique.random_int())),
                           fecha=self.data_factory.date_object())
        self.session.add(self.gasto)
        self.session.commit()
        self.gasto.actividad = self.actividad.id
        self.gasto.viajero = self.viajero1.id
        self.session.commit()
        viajeros=({"Nombre": self.viajero1.nombre, "Apellido": self.viajero1.apellido})
        self.session.commit()
        self.assertEqual(Crear_gasto.poblar_viajero(self.gasto.id), viajeros)

    def test_editar_gasto(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                               apellido=self.data_factory.unique.last_name())
        persona = (self.viajero.nombre + " " + self.viajero.apellido)
        self.session.add(self.viajero)
        self.session.commit()
        concepto = self.data_factory.unique.word()
        valor = (float(self.data_factory.unique.random_int()))
        fecha = self.data_factory.date_object()
        actividad = self.actividad.id
        self.Crear_gasto.crear_gasto(self,actividad, concepto, fecha, valor, persona)
        concepto1 = self.data_factory.unique.word()
        self.Crear_gasto.editar_gasto(self, concepto1, fecha, valor, persona)
        consulta1 = self.session.query(Gasto).filter(Gasto.concepto == concepto1, Gasto.actividad == actividad,
                                                     Gasto.viajero == self.viajero.id).first()
        self.assertEqual(consulta1.concepto, concepto1)

    def test_no_crear_vacios(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                               apellido=self.data_factory.unique.last_name())
        persona = (self.viajero.nombre+" "+self.viajero.apellido)
        self.session.add(self.viajero)
        self.session.commit()
        concepto = self.data_factory.unique.word()
        valor = (float(self.data_factory.unique.random_int()))
        fecha = self.data_factory.date_object()
        actividad=self.actividad.id
        self.Crear_gasto.crear_gasto(actividad,concepto,fecha,valor,persona)
        concepto1 = ""
        consulta=self.Crear_gasto.editar_gasto(self, concepto1, fecha, valor, persona)
        self.assertEqual(consulta, False)

    def test_limite_editar(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                               apellido=self.data_factory.unique.last_name())
        persona = (self.viajero.nombre + " " + self.viajero.apellido)
        self.session.add(self.viajero)
        self.session.commit()
        concepto = self.data_factory.unique.word()
        valor = (float(self.data_factory.unique.random_int()))
        fecha = self.data_factory.date_object()
        actividad = self.actividad.id
        self.Crear_gasto.crear_gasto(actividad, concepto, fecha, valor, persona)
        concepto1 = self.data_factory.pystr(min_chars=256, max_chars=300)
        consulta = self.Crear_gasto.editar_gasto(self, concepto1, fecha, valor, persona)
        self.assertEqual(consulta, False)

    def test_valor_numerico(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                               apellido=self.data_factory.unique.last_name())
        persona = (self.viajero.nombre + " " + self.viajero.apellido)
        self.session.add(self.viajero)
        self.session.commit()
        concepto = self.data_factory.unique.word()
        valor = (float(self.data_factory.unique.random_int()))
        fecha = self.data_factory.date_object()
        actividad = self.actividad.id
        self.Crear_gasto.crear_gasto(actividad, concepto, fecha, valor, persona)
        valor3 = self.data_factory.date_object()
        consulta = self.Crear_gasto.editar_gasto(self, concepto, fecha, valor3, persona)
        self.assertEqual(consulta, False)