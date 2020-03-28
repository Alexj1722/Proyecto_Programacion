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
        self.windowTitle("Gestion de clientes")
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
        self.main_layout = QHBoxLayout()
        self.left_layout = QFormLayout()
        self.right_main_layout = QVBoxLayout()
        self.right_top_layout = QHBoxLayout()
        self.right_bottom_layout = QHBoxLayout()
        
        #Agregar los layout hijos al padre
        self.right_main_layout.addLayout(self.right_top_layout)
        self.right_main_layout.addLayout(self.right_bottom_layout)
        self.main_layout.addLayout(self.left_layout,50)
        self.main_layout.addLayout(self.right_main_layout,70)
        
        #Colocar el layout principal en la ventana principal
        self.setLayout(self.main_layout)

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    
    main()
   