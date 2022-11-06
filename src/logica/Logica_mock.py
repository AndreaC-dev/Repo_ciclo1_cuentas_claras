'''
Esta clase es tan sólo un mock con datos para probar la interfaz
'''
class Logica_mock():

    def __init__(self):
        #Este constructor contiene los datos falsos para probar la interfaz
        nombre1 = "Pepe"
        apellido1 = "Pérez"
        nombre2 = "Ana"
        apellido2 = "Andrade"
        nombre3 = "Pedro"
        apellido3 = "Navajas"
        actividad1 = "Actividad 1"
        actividad2 = "Actividad 2"
        actividad3 = "Actividad 3"
        fecha="12-12-2020"
        self.actividades = [actividad2, actividad3, actividad1]
        self.viajeros = [{"Nombre":nombre1, "Apellido":apellido1}, {"Nombre":nombre2, "Apellido":apellido2}]
        self.gastos = [{"Concepto":"Gasto 1", "Fecha": fecha, "Valor": 10000, "Nombre": nombre1, "Apellido": apellido1}, {"Concepto":"Gasto 2", "Fecha": fecha, "Valor": 20000, "Nombre":nombre2, "Apellido":apellido2}]
        self.matriz = [["", nombre1 + " " + apellido1, nombre2 + " " + apellido2, nombre3 + " " + apellido3 ],[nombre1 + " " + apellido1, -1, 1200, 1000],[nombre2 + " " + apellido2, 0, -1, 1000], [nombre3 + " " + apellido3, 0, 0, -1]]
        self.gastos_consolidados = [{"Nombre": nombre1, "Apellido":apellido1, "Valor":15000}, {"Nombre":nombre2, "Apellido":apellido2, "Valor":12000},{"Nombre":nombre3, "Apellido":apellido3, "Valor":0}]
        self.viajeros_en_actividad = [{"Nombre": nombre1 + " " + apellido1, "Presente":True}, {"Nombre": nombre2 + " " + apellido2, "Presente":True}, {"Nombre":nombre3 + " " + apellido3, "Presente":False}]
