import time
import sys
from   PyQt5.QtCore    import pyqtSlot
from   PyQt5           import QtWidgets
from   PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
from   PyQt5.QtWidgets import *
from   PyQt5.uic       import loadUi

d  = QDialog()
b1 = QPushButton("Click", d)
b1.move(50, 50)
d.setWindowTitle("Dialog")
#d.setWindowModality(Qt.ApplicationModal)
d.exec_()
