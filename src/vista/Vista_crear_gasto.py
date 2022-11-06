from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from functools import partial
from src.logica.crear_gasto import Crear_gasto


class Dialogo_crear_gasto(QDialog):
    #Diálogo para crear o editar un gasto

    def __init__(self,viajeros, gasto,actividad,viajero):
        """
        Constructor del diálogo
        """   
        super().__init__()

        
        self.setFixedSize(340, 250)
        self.setWindowIcon(QIcon("src/devcuentasclaras/recursos/smallLogo.png"))

        self.resultado = ""
        self.viajeros = viajeros

        self.widget_lista = QListWidget()
        

        distribuidor_dialogo = QGridLayout()
        self.setLayout(distribuidor_dialogo)
        numero_fila=0
        
        #Si el diálogo se usa para crear o editar, el título cambia.

        titulo=""
        if(gasto==None):
            titulo="Nuevo Gasto"
        else:
            titulo="Editar Gasto"
      

        self.setWindowTitle(titulo)

        #Creación de las etiquetas y campos de texto

        etiqueta_concepto=QLabel("Concepto")
        distribuidor_dialogo.addWidget(etiqueta_concepto,numero_fila,0,1,3)                
        numero_fila=numero_fila+1

        self.concepto=QLineEdit(self)
        distribuidor_dialogo.addWidget(self.concepto,numero_fila,0,1,3)
        numero_fila=numero_fila+1

        etiqueta_fecha=QLabel("Fecha")
        distribuidor_dialogo.addWidget(etiqueta_fecha,numero_fila,0,1,3)                
        numero_fila=numero_fila+1

        #Campo fecha es un elemento especial para modificar fechas
        self.fecha=QDateEdit(self)
        distribuidor_dialogo.addWidget(self.fecha,numero_fila,0,1,3)
        numero_fila=numero_fila+1

        etiqueta_valor=QLabel("Valor")
        distribuidor_dialogo.addWidget(etiqueta_valor,numero_fila,0,1,3)                
        numero_fila=numero_fila+1

        self.valor=QLineEdit(self)
        distribuidor_dialogo.addWidget(self.valor,numero_fila,0,1,3)
        numero_fila=numero_fila+1

        etiqueta_viajero=QLabel("Viajero")
        distribuidor_dialogo.addWidget(etiqueta_viajero,numero_fila,0,1,3)                
        numero_fila=numero_fila+1


        self.lista_viajeros = QComboBox(self)

        viajeros = Crear_gasto.mostrar_nombre_viajeros_actividad_ordenado(actividad)
        
        for usuario in viajeros:
            self.lista_viajeros.addItem(usuario["Nombre"] + " " +usuario["Apellido"])

        distribuidor_dialogo.addWidget(self.lista_viajeros,numero_fila,0,1,3)
        numero_fila=numero_fila+1

        #Creación de los botones para guardar o cancelar


        self.btn_guardar = QPushButton("Guardar")
        distribuidor_dialogo.addWidget(self.btn_guardar ,numero_fila,1)
        self.btn_guardar.clicked.connect(partial(self.guardar,actividad,self.concepto, self.fecha, self.valor, self.lista_viajeros))

        self.btn_cancelar = QPushButton("Cancelar")
        distribuidor_dialogo.addWidget(self.btn_cancelar ,numero_fila,2)
        self.btn_cancelar.clicked.connect(self.cancelar)


        #Si el diálogo se usa para editar, se debe poblar con la información del gasto a editar
        if gasto != None:
            usuario_app = Crear_gasto.poblar_viajero(gasto.id, actividad)
            self.concepto.setText(gasto.concepto)
            self.fecha.setDate(QDate.fromString((str(gasto.fecha)),'yyyy-MM-dd'))
            self.valor.setText(str(gasto.valor))
            indice = self.lista_viajeros.findText(usuario_app["Nombre"]+" "+usuario_app["Apellido"])
            self.lista_viajeros.setCurrentIndex(indice)

            self.btn_guardar = QPushButton("Guardar")
            distribuidor_dialogo.addWidget(self.btn_guardar, numero_fila, 1)
            self.btn_guardar.clicked.connect(
                partial(self.guardar_editado, actividad,gasto, self.concepto, self.fecha, self.valor, self.lista_viajeros))

            self.btn_cancelar = QPushButton("Cancelar")
            distribuidor_dialogo.addWidget(self.btn_cancelar, numero_fila, 2)
            self.btn_cancelar.clicked.connect(self.cancelar)
    
    def guardar(self,actividad,concepto,fecha, valor,viajeros):
        """
        Esta función envía la información de que se han guardado los cambios
        """
        resultado = Crear_gasto.crear_gasto_listo(actividad, concepto.text(), fecha.date(), valor.text(),viajeros.currentText())
        if resultado==False:
            resultado=0
        else:
            resultado=1
        self.close()
        return resultado

    def guardar_editado(self,actividad, gasto,concepto,fecha, valor,viajeros):
        """
        Esta función envía la información de que se han guardado los cambios
        """
        Crear_gasto.editar_gasto_listo(actividad,gasto, concepto.text(), fecha.date(), valor.text(),viajeros.currentText())
        self.close()

    def cancelar(self):
        """
        Esta función envía la información de que se ha cancelado la operación
        """   
        self.resultado=0
        self.close()
        return self.resultado

