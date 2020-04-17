# -*- coding: utf-8 -*-
#Nombre: Sistema.py
#Funcionalidad: Sistema de gestion de clientes de una tienda
#Autores: Alex Javier Mendoza
#         Darwin Rodriguez Ventura
#         Edi Manrique Ortíz
#         Josue David Nolasco
#Fecha: 27/03/2020

import sqlite3
from sqlite3 import Error
import os
import sys
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import *
import qdarkstyle

class Main(QWidget):
    """ Ventana principal del programa """
    def __init__(self):
        super().__init__()
        #empezamos creando o abriendo la conexion a la base de datos
        self.cliente_db = Cliente_DB("Clientes.db")
        self.setWindowTitle("Gestion de clientes")
        self.showMaximized()
        self.UI()
        self.show()
        
    def UI(self):
        """Creacion de los objetos que componen la interfaz del programa"""
        self.main_design()
        self.layouts()
        self.set_lista_Clientes()
        
        
    def main_design(self):
        """Diseño del formulario principal"""
        self.lista_Clientes = QListWidget()
        
        #self.lista_Clientes.itemClicked.connect(self.show_cliente)
        self.btn_nuevo = QPushButton("Nuevo")
        self.btn_nuevo.clicked.connect(self.agregar_cliente)
        self.btn_nuevo.setStyleSheet("font-size: 15px; background-color: orange; color: white;")
        
        #Boton Actualizar
        self.btn_Actualizar = QPushButton("Actualizar")
        self.btn_Actualizar.clicked.connect(self.set_lista_Clientes)
        self.btn_Actualizar.setStyleSheet("font-size: 15px; background-color: orange; color: white;")
        
        #Boton para eliminar cliente
        self.btn_Eliminar = QPushButton("Eliminar")
        self.btn_Eliminar.clicked.connect(self.eliminarCliente)
        self.btn_Eliminar.setStyleSheet("font-size: 15px; background-color: orange; color: white;")
        
    def layouts(self):
        """Layouts que componen el programa"""
        #Layouts
        self.main_layout = QHBoxLayout()
        self.left_layout = QFormLayout()
        self.right_main_layout = QVBoxLayout()
        self.right_top_layout = QHBoxLayout()
        self.right_bottom_layout = QHBoxLayout()
        
        #Agregar los layout hijos al padre
        self.right_main_layout.addLayout(self.right_top_layout)
        self.right_main_layout.addLayout(self.right_bottom_layout)
        self.main_layout.addLayout(self.left_layout,25)
        self.main_layout.addLayout(self.right_main_layout,75)
        
        #Asignar widgets a los layouts
        self.right_top_layout.addWidget(self.lista_Clientes)
        self.left_layout.addWidget(self.btn_nuevo)
        self.left_layout.addWidget(self.btn_Actualizar)
        self.left_layout.addWidget(self.btn_Eliminar)
        
        #Colocar el layout principal en la ventana principal
        self.setLayout(self.main_layout)
        
        
     #David   
    def agregar_cliente(self):
        """inicia el formulario para agregar un nuevo cliente"""
        self.nuevo_cliente = AgregarCliente(self.cliente_db)
        self.close()
        
    def set_lista_Clientes(self):
        """Se obtiene la lista de clientes y se muestra"""
        clientes_list = self.cliente_db.todos_clientes()
        
        if clientes_list:
            for Clientes in clientes_list:
                self.lista_Clientes.addItem(
                    "{0} --- {1} --- {2} --- {3} --- {4} --- {5} --- {6} --- {7}".format(Clientes[0], Clientes[1], Clientes[2], 
                                                                                 Clientes[3], Clientes[4], Clientes[5], Clientes[6],
                                                                                 Clientes[7]))
    
    
    def eliminarCliente(self):
        
        if self.lista_Clientes.selectedItems():
            cliente = self.lista_Clientes.currentItem().text()
            id = cliente.split(" --- ")[0]
            cliente = self.cliente_db.idcliente(id)
            yes = QMessageBox.Yes
            
            if cliente:
                texto_pregunta = f"¿Está seguro de eliminar el cliente {cliente[1]}"
                pregunta = QMessageBox.question(self, "Advertencia", texto_pregunta,
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                
                if pregunta == QMessageBox.Yes:
                    self.cliente_db.eliminar_ClienteID(cliente[0])
                    QMessageBox.information(self, "Informacion", "Cliente Eliminado con exito")
            else:
                QMessageBox.information(self, "Advertencia", "Ha ocurrido un error. Reintente nuevamente")
        else:
            QMessageBox.information(self, "Advertencia", "Favor seleccionar un empleado a eliminar")

class Cliente_DB:
    """Creacion de la base de datos en SQLite para los clientes. """
    
    def __init__(self, db_nombre):
        """ Inicializador de la clase"""
        self.conexion = self.create_conection(db_nombre)
        self.cliente_query = """ CREATE TABLE IF NOT EXISTS Clientes(
                                    id integer PRIMARY KEY,
                                    nombre text NOT NULL,
                                    apellido text NOT NULL,
                                    sexo text NOT NULL,
                                    fecha_Nacimiento text NOT NULL,
                                    correo text NOT NULL,
                                    telefono text NOT NULL,
                                    direccion text
                                );
                            """ 
        
#        self.constraint_telefono = """ ALTER TABLE Clientes WITH CHECK
#                                        ADD CONSTRAINT CHK_NumeroTelefonico
#		                                CHECK (telefono LIKE '[8-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]' 
#                                       OR telefono LIKE '[3-3][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]')
#                                   """
#                                  
#       self.constraint_genero = """ ALTER TABLE Clientes WITH CHECK
#                               ADD CONSTRAINT CHK_Genero
#                              CHECK (sexo LIKE '%F%' OR sexo LIKE '%M%' )
#                         """    
        self.create_table(self.conexion, self.cliente_query)
#        self.create_table(self.conexion, self.constraint_telefono)
#        self.create_table(self.conexion, self.constraint_genero)
        
                   
    #Edi    
    def create_conection(self, db_nombre):
        """Crear la conexion a la base de datos SQLite. """
        conexion=None
        
        #Intento de conectar
        try:
            conexion = sqlite3.connect(db_nombre)
            print("Conexion realizada. Version {}".format(sqlite3.version))
        except Error as e:
            print (e)
        finally: 
            return conexion
    
    def create_table(self, conexion, query):
        """
        crea una tabla basada en los valores de query 
        Parametros:
        conexion: Conexion a la base de datos.
        query: contiene la instrucion de CREATE QUERY
        return: 
        """
        try:
            cursor= conexion.cursor()
            cursor.execute(query)
        except Error as e:
            print (e)        
            
    def insertCliente(self, clientee):
        sqlinsert = """
                    INSERT INTO Clientes(
                        id, nombre, apellido, sexo,
                        fecha_Nacimiento, correo, telefono, direccion )
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?) 
                        """
        try: 
            cursor = self.conexion.cursor()
            cursor.execute(sqlinsert, clientee)
            self.conexion.commit()
        except Error as e:
            print (e)       
            
            
    def todos_clientes(self):
        """Obtiene todas las tuplas de la tabla de clientes"""
        sqlQuery = " SELECT * FROM Clientes ORDER BY ROWID ASC"
      
        try:
            cursor = self.conexion.cursor()
            clientes_l = cursor.execute(sqlQuery).fetchall()
            return clientes_l
        except Error as e:
            print(e)
            
        return None        
    
    def idcliente(self, id):
        sqlQuery = "SELECT * FROM Clientes WHERE id = ?"
        
        try:
            cursor = self.conexion.cursor()
            cliente = cursor.execute(sqlQuery, (id,)).fetchone()
            return cliente
        except Error as e:
            print (e)
            
        return None
    
    def eliminar_ClienteID(self, id):
        """
        Elimina a un cliente mediante el valir de su id,
        """
        sqlQuery = "DELETE FROM Clientes WHERE id = ? "
        
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sqlQuery, (id,))
            self.conexion.commit()
            
            return True
        except Error as e:
            print(e)
            
        return None 
    
class AgregarCliente(QWidget):
    def __init__(self, cliente_db):
        super().__init__()
        self.cliente_db = cliente_db
        self.setWindowTitle("Formulario para Gestion de clientes")
        self.setGeometry(500,200,500,400)
        self.UI()
        self.show()
        
    def UI(self):
        self.mainDesign()
        self.layouts()
    
    def mainDesign(self):
        
       #Titulo del widget
        self.Titulo = QLabel("Agregar Cliente")
        self.Titulo.setFont(QFont('SansSerif',25))
        #self.Titulo.setText("LikeGreeks")

        self.imgUser = QLabel()
        self.imgUser.setPixmap(QPixmap("team.png"))
       

        #Botones del widget para clientes
        # widget para nombre
        self.label = QLabel("")
        self.label.setStyleSheet("background-color: yellow;")
        self.label_nombre = QLabel("Nombre: ")
        self.label_nombre.setFont(QFont("Arial",12))
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("-----------")
        self.input_nombre.setStyleSheet("background-color: white; color: Black;")
        
        # widget para nombre
        self.label = QLabel("")
        self.label.setStyleSheet("background-color: yellow;")
        self.label_id = QLabel("Id:")
        self.label_id.setFont(QFont("Arial",12))
        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("00")
        self.input_id.setStyleSheet("background-color: white; color: Black;")

        # widget para apellido
        self.label_Apellido = QLabel("Apellido:")
        self.label_Apellido.setFont(QFont("Arial",12))
        self.input_Apellido = QLineEdit()
        self.input_Apellido.setPlaceholderText("---------------")
        self.input_Apellido.setStyleSheet("background-color: white; color: Black;")

        # widget para Genero
        self.label_sexo = QLabel("Genero:")
        self.label_sexo.setFont(QFont("Arial",12))
        self.input_sexo = QLineEdit()
        self.input_sexo.setPlaceholderText("M ó F")
        self.input_sexo.setStyleSheet("background-color: white; color: Black;")

        # widget para telefono
        self.label_telefono = QLabel("Telefono:")
        self.label_telefono.setFont(QFont("Arial",12))
        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("0000-0000")
        self.input_telefono.setStyleSheet("background-color: white; color: Black;")

        # widget para correo
        self.label_correo = QLabel("Gmail:")
        self.label_correo.setFont(QFont("Arial",12))
        self.input_correo = QLineEdit()
        self.input_correo.setPlaceholderText("address@gmail.com")
        self.input_correo.setStyleSheet("background-color: white; color: Black;")


        # widget para direccion
        self.label_direccion = QLabel("Direccion:")
        self.label_direccion.setFont(QFont("Arial",12))
        self.textedit_direc = QLineEdit()
        self.textedit_direc.setStyleSheet("background-color: white; color: Black;")


        # widget para fechanacimiento
        self.label_fecNacimiento = QLabel("Fecha Nacimiento:")
        self.label_fecNacimiento.setFont(QFont("Arial",12))
        self.input_fechNacimiento = QLineEdit()
        self.input_fechNacimiento.setPlaceholderText("dd/mm/yyyy")
        self.input_fechNacimiento.setStyleSheet("background-color: white; color: Black;")

        # widget para btn aceptar
        self.btn_Aceptar = QPushButton("Aceptar")
        self.btn_Aceptar.clicked.connect(self.IngresaCliente)
        self.btn_Aceptar.setGeometry(5,50,50,15)
        self.btn_Aceptar.setStyleSheet("font-size: 15px; background-color: red; color: white;")

        # widget para btn regresar
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.clicked.connect(self.IngresaCliente)
        self.btn_regresar.setGeometry(5,50,50,15)
        self.btn_regresar.setStyleSheet("font-size: 15px; background-color: red; color: white;")

 
    def layouts(self):
        
        #Diseño Principal
        self.main_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.btn_layout = QFormLayout()
        
        #Agregar los widgets hijos al padre
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.btn_layout)
        
        #Agregar los widgets al top_layout
        self.top_layout.addWidget(self.Titulo)
        
        #agregar los widgets al btn_layout
        self.btn_layout.addRow(self.label_id, self.input_id)
        self.btn_layout.addRow(self.label_nombre, self.input_nombre)
        self.btn_layout.addRow(self.label_Apellido, self.input_Apellido)
        self.btn_layout.addRow(self.label_sexo, self.input_sexo)
        self.btn_layout.addRow(self.label_telefono, self.input_telefono)
        self.btn_layout.addRow(self.label_fecNacimiento, self.input_fechNacimiento)
        self.btn_layout.addRow(self.label_correo, self.input_correo)
        self.btn_layout.addRow(self.label_direccion, self.textedit_direc)
        self.btn_layout.addRow("", self.btn_Aceptar)
        self.btn_layout.addRow("", self.btn_regresar)
        
        self.setLayout(self.main_layout)
        
    def IngresaCliente(self):
        if(self.input_nombre.text() or self.input_Apellido.text()
           or self.input_sexo.text() or self.textedit_direc.text()
           or self.input_telefono.text() or self.input_correo.text()
           or self.input_fechNacimiento.text () != "" ):
            Clientes = (self.input_id.text(), self.input_nombre.text(), self.input_Apellido.text(),
                        self.input_sexo.text(), self.input_fechNacimiento.text(),
                        self.input_correo.text(), self.input_telefono.text(),
                        self.textedit_direc.text() )
            try:
                self.cliente_db.insertCliente(Clientes)
                QMessageBox.information(
                    self,"Informacion", "Cliente agregado con exito")
                self.close()
                self.main = Main()
            except Error as e:
                QMessageBox.information(
                    self, "Error", "Error al ingresar cliente")
        
        else:
            QMessageBox.information(self,"iNFORMACION", "Error se alvido agregar revisa")
            self.label_nombre.setStyleSheet("Color:red;") 
            self.label_Apellido.setStyleSheet("Color:red;") 
            self.label_correo.setStyleSheet("Color:red;") 
            self.label_direccion.setStyleSheet("Color:red")
            self.label_fecNacimiento.setStyleSheet("Color:red")
            self.label_sexo.setStyleSheet("Color:red")
            self.label_telefono.setStyleSheet("Color:red")

"""class BuscarCliente (QWidget):
     def __init__(self):
         super().__init__()
         self.setWindowTitle("Buscador de Cliente") 
         self.setGeometry(100,50,100,50)
         self.UI()
         self.show()
         
    def UI(self):
        self.mainDesign()
        self.Layouts()
        
    def main_design(self):
        self.Titulo = QLabel("Buscar Cliente")
        self.Titulo.setFont(QFont'SanSerif', 25)
    
        self.label = QLabel("")
        self.label.setStyleSheet("background-color: Orange;")
        self.label_id = QLabel("Ingrese Id para buscar: ")
        self.label_id.setFont(QFont("Arial", 12))
        self.input_id = QLineEdit() 
        self.input_id.setPlaceholderText("00")
        self.input_id.setStyleSheet("background-color: white;")
        
        self.btn_buscar = QPushButton("Buscar ")
        self.btn_buscar.clicked.connect(self.buscar)
        self.btn_buscar.setGeometry(25, 10, 25, 10)
        
    def layouts(self):
        self.main_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        selt.btn_layout = QForm()
        
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.btn_layout)
        
        self.top_layout.addWidget(self.Titulo)
        
        self.btn_layout.addRow(self.label)
        self.btn_layout.addRow(self.label_id, self.input_id)
        self.btn_layout.addRow(self.btn_buscar)
        
        self.setLayout(self.main_layout)
        
    def buscar(self):
        if(self.input_id.text() != " "):
            QMessageBox.information(self, "Informacion", "Cliente encontrado")
        else:
            QMessageBox.information(self, "Informacion", "Ingrese id porfavor")
"""    
                        
 
 
                            
def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = Main()
    window.showMaximized()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
   