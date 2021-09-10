from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from functools import partial
from src.logica.crear_actividad import Crear_Actividad

class Dialogo_crear_actividad(QDialog):
    #Diálogo para crear una actividad

    def __init__(self, actividad):
        """
        Constructor del diálogo
        """    
        super().__init__()

        self.setFixedSize(300,110)
        
        self.setWindowIcon(QIcon("src/recursos/smallLogo.png"))

        self.resultado = ""

        self.widget_dialogo = QListWidget()

        distribuidor_dialogo = QGridLayout()
        self.setLayout(distribuidor_dialogo)
        numero_fila=0
        
        #El título del diálogo varía si se usa para crear o editar una actividad

        titulo=""
        if actividad is None:
            titulo="Nueva Actividad"
        else:
            titulo="Editar Actividad"
        self.setWindowTitle(titulo)
        
        #Creación de las etiquetas

        etiqueta_nombre=QLabel("Nombre")
        distribuidor_dialogo.addWidget(etiqueta_nombre,numero_fila,0,1,3)                
        numero_fila=numero_fila+1

        self.texto_nombre=QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_nombre,numero_fila,0,1,3)
        numero_fila=numero_fila+1

        # Si el diálogo se usa para editar, se debe mostrar el nombre de la actividad a editar
        es_editar = True
        if (actividad != None):
            self.texto_nombre.setText(actividad.nombre)
            self.texto_nombre.textChanged.connect(
                lambda: self.btn_guardar.setEnabled(self.habilitar_guardado(self.texto_nombre)))
        else:
            es_editar = False
            self.texto_nombre.textChanged.connect(
                lambda: self.btn_guardar.setEnabled(self.habilitar_guardado(self.texto_nombre)))

        #Creación de los botones
        
        self.btn_guardar = QPushButton("Guardar")
        distribuidor_dialogo.addWidget(self.btn_guardar ,numero_fila,1)
        self.btn_guardar.clicked.connect(partial(self.guardar, self.texto_nombre, es_editar, actividad))

        self.btn_cancelar = QPushButton("Cancelar")
        distribuidor_dialogo.addWidget(self.btn_cancelar ,numero_fila,2)
        self.btn_cancelar.clicked.connect(self.cancelar)

    def habilitar_guardado(self, nombre):
        if len(nombre.text()) > 0:
            return True
        else:
            return False

    def guardar(self, nombre, es_editar, actividad):
        """
        Esta función envía la información de que se han guardado los cambios
        """
        if es_editar:
            if not Crear_Actividad.validar_actividad_no_repetida(nombre.text()):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("El nombre ya existe")
                msg.setInformativeText('Por favor escoja otro nombre')
                msg.setWindowTitle("Nombre duplicado")
                msg.exec_()
                return 0
            else:
                Crear_Actividad.editar_actividad(nombre.text(), actividad)
                self.resultado = 1
            self.close()
            return self.resultado

        Crear_Actividad.crear_nueva_actividad(nombre.text())
        self.resultado = 1
        self.close()
        return self.resultado


    def cancelar(self):
        """
        Esta función envía la información de que se ha cancelado la operación
        """ 
        self.resultado=0
        self.close()
        return self.resultado


