# -*- coding: utf-8 -*-
#Nombre: Sistema.py
#Funcionalidad: Sistema de gestion de clientes de una tienda
#Autores: Alex Javier Mendoza
#         Darwin Rodriguez Ventura
#         Edi Manrique Ortíz
#          Josue David Nolasco
#Fecha: 27/03/2020

import sqlite3
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QTime, QTimer
from PyQt5.QtWidgets import *

cliente_id = None

class Main(QWidget):
    """ Ventana principal del programa """
    def __init__(self):
        super().__init__()
        self.windowTitle("Gestion de clientes")
        self.setGeometry(550,250,850,700)
        self.UI()
        self.show()
        # Crear conecion a la base de datos"
        
        


def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())
    
if --name-- == "__main__":
    main()