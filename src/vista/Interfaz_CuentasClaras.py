from PyQt5.QtWidgets import QApplication
from .Vista_lista_actividades import Vista_lista_actividades
from .Vista_lista_viajeros import Vista_lista_viajeros
from .Vista_actividad import Vista_actividad
from .Vista_reporte_compensacion import Vista_reporte_compensacion
from .Vista_reporte_gastos import Vista_reporte_gastos_viajero
from src.logica.listado_actividades import Listado_actividades
from src.logica.crear_actividad import Crear_Actividad
from .Vista_agregar_viajero import Dialogo_agregar_viajeros

class App_CuentasClaras(QApplication):
    """
    Clase principal de la interfaz que coordina las diferentes vistas/ventanas de la aplicación
    """

    def __init__(self, sys_argv, logica):
        """
        Constructor de la interfaz. Debe recibir la lógica e iniciar la aplicación en la ventana principal.
        """
        super(App_CuentasClaras, self).__init__(sys_argv)
        
        self.logica = logica
        self.mostrar_vista_lista_actividades()
        
        
    def mostrar_vista_lista_actividades(self):
        """
        Esta función inicializa la ventana de la lista de actividades
        """
        self.vista_lista_actividades = Vista_lista_actividades(self) 
        self.vista_lista_actividades.mostrar_actividades()


    def insertar_actividad(self, nombre):
        """
        Esta función inserta una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.vista_lista_actividades.mostrar_actividades()

    def editar_actividad(self):
        """
        Esta función editar una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.vista_lista_actividades.mostrar_actividades()

    def eliminar_actividad(self, actividad):
        """
        Esta función elimina una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        Crear_Actividad.eliminar_actividad(actividad)
        self.vista_lista_actividades.mostrar_actividades()


    def mostrar_viajeros(self):
        """
        Esta función muestra la ventana de la lista de viajeros
        """
        self.vista_lista_viajeros=Vista_lista_viajeros(self)
        self.vista_lista_viajeros.mostrar_viajeros(self.logica.viajeros)

    def insertar_viajero(self, nombre, apellido):
        """
        Esta función inserta un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.viajeros.append({"Nombre":nombre, "Apellido":apellido})
        self.vista_lista_viajeros.mostrar_viajeros(self.logica.viajeros)

    def editar_viajero(self, indice_viajero, nombre, apellido):
        """
        Esta función edita un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """        
        self.logica.viajeros[indice_viajero] = {"Nombre":nombre, "Apellido":apellido}
        self.vista_lista_viajeros.mostrar_viajeros(self.logica.viajeros)

    def eliminar_viajero(self, indice_viajero):
        """
        Esta función elimina un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.viajeros.pop(indice_viajero)
        self.vista_lista_viajeros.mostrar_viajeros(self.logica.viajeros)
    
    def mostrar_actividad(self, actividad):
        """
        Esta función muestra la ventana detallada de una actividad
        """
        self.vista_actividad = Vista_actividad(self, actividad)
        self.vista_actividad.mostrar_gastos_por_actividad(actividad)

    def insertar_gasto(self, concepto, fecha, valor, viajero_nombre, viajero_apellido):
        """
        Esta función inserta un gasto a una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.gastos.append({"Concepto":concepto, "Fecha": fecha, "Valor": int(valor), "Nombre": viajero_nombre, "Apellido": viajero_apellido})
        self.vista_actividad.mostrar_gastos_por_actividad()

    def editar_gasto(self, actividad):
        """
        Esta función edita un gasto de una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.vista_actividad.mostrar_gastos_por_actividad(actividad)

    def eliminar_gasto(self, indice):
        """
        Esta función elimina un gasto de una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.gastos.pop(indice)
        self.vista_actividad.mostrar_gastos_por_actividad(self.logica.actividades[self.actividad_actual], self.logica.gastos)

    def mostrar_reporte_compensacion(self, actividad):
        """
        Esta función muestra la ventana del reporte de compensación
        """
        self.vista_reporte_comensacion = Vista_reporte_compensacion(self, actividad)
        self.vista_reporte_comensacion.mostrar_reporte_compensacion(actividad)

    def mostrar_reporte_gastos_viajero(self, actividad):
        """
        Esta función muestra el reporte de gastos consolidados
        """
        self.vista_reporte_gastos = Vista_reporte_gastos_viajero(self, actividad)
        self.vista_reporte_gastos.mostar_reporte_gastos(actividad)

    def actualizar_viajeros(self, viajeros,actividad):
        """
        Esta función añade un viajero a una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.listado = Listado_actividades()
        self.listado.agregar_viajero_con_check(viajeros, actividad)

    def dar_viajeros(self):
        """
        Esta función pasa la lista de viajeros (debe implementarse como una lista de diccionarios o str)
        """
        return self.logica.viajeros

    def terminar_actividad(self, indice):
        """
        Esta función permite terminar una actividad (debe implementarse)
        """
        pass