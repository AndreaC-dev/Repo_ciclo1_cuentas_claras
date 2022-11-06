import unittest
__author__ = "Andrea Cardenas y Daniel Velasquez"
__copyright__ = "Andrea y Daniel"
__license__ = "mit"
from src.logica.listado_actividades import Listado_actividades
from src.modelo.declarative_base import Session
from src.modelo.actividad import Actividad
from src.modelo.viajero import Viajero
from src.modelo.viajero import ActividadViajero
from faker import Faker

class ListadoActividadesTestCase(unittest.TestCase):
    def setUp(self):
        self.Listado_actividades = Listado_actividades()
        self.session = Session()
        self.data_factory = Faker()

    def tearDown(self):
        self.session = Session()
        busqueda = self.session.query(Actividad).all()
        for actividad in busqueda:
            self.session.delete(actividad)
        self.session.commit()
        self.session = Session()
        busqueda = self.session.query(Viajero).all()
        for viajero in busqueda:
            self.session.delete(viajero)
        self.session.commit()
        self.session.close()

    def test_ordenar_vacio(self):
        arreglo_prueba = []
        self.assertEqual(Listado_actividades.ordenar_lista_actividades(arreglo_prueba), [])

    def test_ordenar_alfabeticamente(self):
        for i in range(1,4):
            lista=[Actividad(nombre=self.data_factory.unique.word())]
        ordenado=sorted(lista)
        self.assertEqual(Listado_actividades.ordenar_lista_nombre_actividades(lista), ordenado)

    def test_validar_almacenamiento(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        esperado=[]
        esperado.append((self.actividad.nombre,))
        self.assertEqual(Listado_actividades.validar_almacenamiento(self.actividad.nombre), esperado)

    def test_mostrar_nombres_actividades(self):
        esperado=[]
        for i in range(1, 10):
            self.actividad = Actividad(nombre=self.data_factory.unique.word())
            self.session.add(self.actividad)
            self.session.commit()
            esperado.append(self.actividad.nombre)
        self.assertEqual(Listado_actividades.mostrar_nombres_actividades(self.actividad), esperado)

    def test_traer_n_viajeros(self):
        viajeros=[]
        for i in range(1, 5):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                              apellido=self.data_factory.unique.last_name())
            self.session.add(self.viajero)
            self.session.commit()
            viajeros.append(self.viajero.nombre + " "+self.viajero.apellido)
        self.assertEqual(Listado_actividades.mostrar_nombre_viajeros(self.viajero), viajeros)


    def test_mostrar_si_viajeros_pertenecen(self):
        viajeros =[]
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        for j in range(1, 2):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                              apellido=self.data_factory.unique.last_name())
            self.session.add(self.viajero)
            self.session.commit()
            self.session.add(ActividadViajero(actividad_id=self.actividad.id, viajero_id=self.viajero.id))
            self.session.commit()
            viajeros.append({"Nombre":self.viajero.nombre + " "+self.viajero.apellido,"Presente": True})
        for i in range(1, 3):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                              apellido=self.data_factory.unique.last_name())
            self.session.add(self.viajero)
            self.session.commit()
            viajeros.append({"Nombre":self.viajero.nombre + " "+self.viajero.apellido,"Presente": False})

        self.session.commit()
        self.assertEqual(Listado_actividades.mostrar_si_viajeros_pertenecen_desorden(self.actividad.id), viajeros)

    def test_agregar_viajero_check(self):
        viajeros =[]
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        for j in range(1, 2):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                              apellido=self.data_factory.unique.last_name())
            self.session.add(self.viajero)
            self.session.commit()
            self.session.add(ActividadViajero(actividad_id=self.actividad.id, viajero_id=self.viajero.id))
            self.session.commit()
            viajeros.append({"Nombre":self.viajero.nombre + " "+self.viajero.apellido,"Presente": True})
        for i in range(1, 3):
            self.viajero = Viajero(nombre=self.data_factory.unique.first_name(),
                              apellido=self.data_factory.unique.last_name())
            self.session.add(self.viajero)
            self.session.commit()
            viajeros.append({"Nombre":self.viajero.nombre + " "+self.viajero.apellido,"Presente": False})
        self.session.commit()
        viajeros[-1]["Presente"]=(True)
        self.assertEqual(Listado_actividades.agregar_viajero_check(self.actividad.id,viajeros), viajeros)
    
    def test_mostrar_actividades(self):
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        self.assertEqual(len(Listado_actividades.mostrar_actividades(self.actividad)), 1)
        
    def test_ordenar_lista_actividades_ordena(self):
        lista =[]
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        lista.append(self.actividad)
        self.actividad = Actividad(nombre=self.data_factory.unique.word())
        self.session.add(self.actividad)
        self.session.commit()
        lista.append(self.actividad)
        ordenado=sorted(lista, key=lambda x: x.nombre)
        self.assertEqual(Listado_actividades.ordenar_lista_actividades(lista), ordenado)



