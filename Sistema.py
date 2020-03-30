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
import qdarkstyle

cliente_id = None

class Main(QWidget):
    """ Ventana principal del programa """
    def __init__(self):
        super().__init__()
        #empezamos creando o abriendo la conexion a la base de datos
        self.cliente_db = Cliente_DB("Clientes.db")
        self.setWindowTitle("Gestion de clientes")
        self.UI()
        self.show()
        
    def UI(self):
        """Creacion de los objetos que componen la interfaz del programa"""
        self.main_design()
        self.layouts()
    
    def main_design(self):
        """Diseño del formulario principal"""
        self.lista_Clientes = QListWidget()
        self.btn_nuevo = QPushButton("Nuevo")
        self.btn_Actualizar = QPushButton("Actualizar")
        self.btn_Eliminar = QPushButton("Eliminar")
        
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

class Cliente_DB:
    """Creacion de la base de datos en SQLite para los clientes. """
    def __init__(self, db_nombre):
        """ Inicializador de la clase"""
        self.conexion = self.create_conection(db_nombre)
        self.cliente_query= """ CREATE TABLE IF NOT EXISTS Clientes(
                                    id integer PRIMARY KEY,
                                    nombre text NOT NULL,
                                    apellido text NOT NULL,
                                    sexo text NOT NULL,
                                    fecha_Nacimiento text NOT NULL,
                                    pais text NOT NULL,
                                    telefono text NOT NULL
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
                            
                            
def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = Main()
    window.showMaximized()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
   