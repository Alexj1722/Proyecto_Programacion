# -*- coding: utf-8 -*-
#Nombre: Sistema.py
#Funcionalidad: Sistema de gestion de clientes de una tienda
#Autores: Alex Javier Mendoza
#         Darwin Rodriguez Ventura
#         Edi Manrique Ortíz
#          Josue David Nolasco
#Fecha: 27/03/2020

import sqlite3
from sqlite3 import Error
import os
import sys
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import *
import qdarkgraystyle

cliente_id = None

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
        self.btn_Actualizar = QPushButton("Actualizar")
        self.btn_Eliminar = QPushButton("Eliminar")
        #self.btn_Eliminar.clicked.connect(self.eliminarCliente)
        
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
        self.create_table(self.conexion, self.cliente_query)
        
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
        self.Titulo = QLabel("Gestion de clientes")
        #Campos y botones del formulario de clientes
        self.label_id = QLabel("id: ")
        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("000")
        self.label_nombre = QLabel("Nombre: ")
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("_ _ _ _ _ _ _ _ _ _ _")
        self.label_Apellido = QLabel("Apellido: ")
        self.input_Apellido = QLineEdit()
        self.input_Apellido.setPlaceholderText("_ _ _ _ _ _ _ _ _ _ _")
        self.label_sexo = QLabel("Sexo: ")
        self.input_sexo = QLineEdit()
        self.input_sexo.setPlaceholderText("M ó F")
        self.label_telefono = QLabel("Telefono: ")
        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("0000-0000")
        self.label_correo = QLabel("Correo: ")
        self.input_correo = QLineEdit()
        self.input_correo.setPlaceholderText("address@gmail.com")
        self.label_fecNacimiento = QLabel("Fecha Nacimiento: ")
        self.input_fecNacimiento = QLineEdit()
        self.input_fecNacimiento.setPlaceholderText("dd/mm/yyyy")
        self.label_direc = QLabel("Direccion: ")
        self.input_direc = QLineEdit()
        self.input_direc.setPlaceholderText("_ _ _ _ _ _ _ _ _ _ _")
        self.btn_Aceptar = QPushButton("Aceptar")
        self.btn_Aceptar.clicked.connect(self.IngresaCliente)
        
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
        self.btn_layout.addRow(self.label_fecNacimiento, self.input_fecNacimiento)
        self.btn_layout.addRow(self.label_correo, self.input_correo)
        self.btn_layout.addRow(self.label_direc, self.input_direc)
        self.btn_layout.addRow(self.btn_Aceptar)
        
        self.setLayout(self.main_layout)
        
    def IngresaCliente(self):
        if(self.input_nombre.text() or self.input_Apellido.text()
           or self.input_sexo.text() or self.input_direc.text()
           or self.input_telefono.text() or self.input_correo.text()
           or self.input_fecNacimiento.text () != "" ):
            Clientes = (self.input_id.text(), self.input_nombre.text(), self.input_Apellido.text(),
                        self.input_sexo.text(), self.input_fecNacimiento.text(),
                        self.input_correo.text(), self.input_telefono.text(),
                        self.input_direc.text() )
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
            QMessageBox.information(
                self, "Informacion", "Debe llenar todos los campos")

                            
                            
def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())
    window = Main()
    window.showMaximized()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
   