import time
import sys
from   PyQt5.QtCore    import pyqtSlot
from   PyQt5           import QtWidgets, QtGui
from   PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
from   PyQt5.QtWidgets import *
from   PyQt5.uic       import loadUi

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setGeometry(300, 300, 300, 220)



class App(QMainWindow):
     def __init__(self):
        super(App, self).__init__()
        try:
            loadUi('interface.ui', self)
        except Exception as e:
            print (e)
            print ("Interface.ui could not be found!")
        self.rowCount       = 0
        self.selectedRow    = 0
        self.selectedColumn = 0
        self.pageCount      = 0
        self.currentPage    = 0
        self.exm            = Example()
     def run(self):
         self.makeTable()
         self.add_button.clicked.connect(self.addBook)
         self.edit_button.clicked.connect(self.editBook)
         self.delete_button.clicked.connect(self.deleteBook)
         self.filter_button.clicked.connect(self.filterBooks)
         self.clear_button.clicked.connect(self.clearFilter)
         self.tableWidget.cellClicked.connect(self.rowSelect)

     def rowSelect(self, row, col):
        print (row, col)
        self.selectedRow = row
        self.selectedColumn = col

     def makeTable(self):
        for x in range(0, 3):
            self.tableWidget.setColumnWidth(x, 315)

     def addBook(self):
        miniDialog  = QDialog()
        miniDialog.setGeometry(500, 500, 400, 300)
        miniDialog.setWindowTitle("Add Book")
        addButton = QPushButton("Add", miniDialog)
        cancelButton =QPushButton("Cancel", miniDialog)
        groupBox   = QGroupBox("Add details", miniDialog)
        author_label = QLabel("Author: ", groupBox)
        author_edit  = QLineEdit(groupBox)

        title_label = QLabel("Title: ", groupBox)
        title_lineEdit = QLineEdit(groupBox)

        year_label = QLabel("Year: ", groupBox)
        year_lineEdit = QLineEdit(groupBox)

        groupBox.setGeometry(10, 10, 381, 211)
        author_edit.setGeometry(100, 20, 251, 31)
        author_label.setGeometry(20, 30, 61, 16)
        title_label.setGeometry(20, 80, 61, 16)
        title_lineEdit.setGeometry(100, 70, 251, 31)
        year_label.setGeometry(20, 120, 61, 31)
        year_lineEdit.setGeometry(100, 120, 251, 31)
        addButton.setGeometry(20, 240, 121, 51)
        cancelButton.setGeometry(160, 240, 121, 51)

        font = QtGui.QFont()
        input_font = QtGui.QFont("Ariel")
        input_font.setPointSize(13)
        font.setBold(True)

        author_label.setFont(font)
        title_label.setFont(font)
        year_label.setFont(font)

        author_edit.setFont(input_font)
        title_lineEdit.setFont(input_font)
        year_lineEdit.setFont(input_font)

        author_edit.setStyleSheet(""" border-radius: 10px; """)
        title_lineEdit.setStyleSheet(""" border-radius:10px;""")
        year_lineEdit.setStyleSheet(""" border-radius:10px;""")

        
        miniDialog.exec_()
        print ("Add Book has been called.")

        book = ["one", "two", "three"]
        rowCount = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowCount)
        self.tableWidget.setRowHeight(rowCount, 75)
        for x in range(0, 3):
            self.tableWidget.setItem(rowCount, x, QtWidgets.QTableWidgetItem(str(book[x])))
        self.rowCount = self.rowCount + 1

     def editBook(self):
        print ("Edit book has been called.")



     def deleteBook(self):
         print ("Delete book has been called.")
         self.tableWidget.removeRow( self.selectedRow )

     def filterBooks(self):
         print ("Filter book has been called.")

     def clearFilter(self):
         print ("Clear filter has been called.")

def main():
    app = QApplication(sys.argv)
    widget = App()
    widget.show()
    widget.run()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
