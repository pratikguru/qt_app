import time
import sys
from       dbHandler       import DBSql
try:
    from   PyQt5             import QtCore
    from   PyQt5.QtCore    import pyqtSlot
    from   PyQt5           import QtWidgets, QtGui
    from   PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
    from   PyQt5.QtWidgets import *
    from   PyQt5.uic       import loadUi
except Exception as e:
    print ("Requirement Error! The PyQt Libs are not installed.")
    import os



class BookDialog():
    def __init__(self, string, btnString):
        self.miniDialog = QDialog()

        self.miniDialog.setGeometry( 500, 500, 400, 300 )
        self.miniDialog.setWindowTitle(str(string))
        self.addButton    = QPushButton(str(btnString), self.miniDialog)
        self.cancelButton = QPushButton("Cancel", self.miniDialog)
        self.groupBox     = QGroupBox("Add details", self.miniDialog)
        self.author_label = QLabel("Author: ", self.groupBox)
        self.author_edit  = QLineEdit(self.groupBox)

        self.title_label    = QLabel("Title: ", self.groupBox)
        self.title_lineEdit = QLineEdit(self.groupBox)

        self.year_label    = QLabel("Year: ", self.groupBox)
        self.year_lineEdit = QLineEdit(self.groupBox)

        self.cancelled = False
        self.isMax99999 = QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]{1,5}$"))
        self.year_lineEdit.setValidator(self.isMax99999)

        self.initUI()


    def initUI(self):
        #Setting up geometry
        self.groupBox.setGeometry(10, 10, 381, 211)
        self.author_edit.setGeometry(100, 20, 251, 31)
        self.author_label.setGeometry(20, 30, 61, 16)
        self.title_label.setGeometry(20, 80, 61, 16)
        self.title_lineEdit.setGeometry(100, 70, 251, 31)
        self.year_label.setGeometry(20, 120, 61, 31)
        self.year_lineEdit.setGeometry(100, 120, 251, 31)
        self.addButton.setGeometry(20, 240, 121, 51)
        self.cancelButton.setGeometry(160, 240, 121, 51)

        #Fonts and customization
        self.font = QtGui.QFont()
        self.input_font = QtGui.QFont("Ariel")
        self.input_font.setPointSize(13)
        self.font.setBold(True)

        self.author_label.setFont(self.font)
        self.title_label.setFont(self.font)
        self.year_label.setFont(self.font)

        self.author_edit.setFont(self.input_font)
        self.title_lineEdit.setFont(self.input_font)
        self.year_lineEdit.setFont(self.input_font)

        self.author_edit.setStyleSheet(""" border-radius: 10px; """)
        self.title_lineEdit.setStyleSheet(""" border-radius:10px;""")
        self.year_lineEdit.setStyleSheet(""" border-radius:10px;""")


    def run(self):
        self.addButton.clicked.connect(self.addBookEmitSignal)
        self.cancelButton.clicked.connect(self.cancelBookEmitSignal)
        self.miniDialog.exec_()

    def addBookEmitSignal(self):
        safeToQuit = True
        if not self.author_edit.text():
            print ("Please add Author.")
            safeToQuit = False
        if not self.title_lineEdit.text():
            print ("Please add Title.")
            safeToQuit = False
        if not self.year_lineEdit.text():
            print ("Please add a Year.")
            safeToQuit = False
        if safeToQuit:
            self.miniDialog.close()

    def cancelBookEmitSignal(self):
         self.cancelled = True
         self.miniDialog.close()


class App(QMainWindow):
     def __init__(self):
        super(App, self).__init__()
        try:
            loadUi('interface.ui', self)
        except Exception as e:
            print (e)
            print ("Interface.ui could not be found!")
        #self.db             = DBHandler("db.txt")
        self.db             = DBSql()
        self.rowCount       = 0
        self.selectedRow    = 0
        self.selectedColumn = 0
        self.pageCount      = 0
        self.currentPage    = 0
        self.addDialog      = BookDialog("Add Book", "Add")
        self.maxRows        = 0
        self.currentRow     = 0
        self.lowerLimit     = 1
        self.upperLimit     = 4
        self.makeTable()

        self.conn = self.db.create_connection("tester.db")
        book = """
                CREATE TABLE IF NOT EXISTS BOOK (
                    AUTHOR TEXT NOT NULL,
                    TITLE  TEXT NOT NULL,
                    YEAR   INTEGER NOT NULL )
               """
        if not self.conn:
            print ("DB Connection failure!")
            return

        books = []
        self.maxRows = self.db.getAll(self.conn)
        self.denom_label.setText(str(int(len(self.maxRows) / 3)))
        print(len(self.maxRows))
        rows  = self.db.getAll(self.conn)
        for count, row in enumerate(rows):
            if count == 3:
                return
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowCount)
            self.tableWidget.setRowHeight(rowCount, 75)
            for x in range(0, 4):
                self.tableWidget.setItem(rowCount, x, QtWidgets.QTableWidgetItem( str(row[x])) )

     def run(self):

         self.add_button.clicked.connect(self.addBook)
         self.edit_button.clicked.connect(self.editBook)
         self.delete_button.clicked.connect(self.deleteBook)
         self.filter_button.clicked.connect(self.filterBooks)
         self.clear_button.clicked.connect(self.clearFilter)
         self.tableWidget.cellClicked.connect(self.rowSelect)
         self.previous_button.clicked.connect(self.previousPage)
         self.next_button.clicked.connect(self.nextPage)

     def nextPage(self):
         if self.currentPage >= len(self.maxRows)/3:
             print ("Upper limit pages reached.")
             return
         self.num_label.setText(str(self.currentPage))
         y = self.currentPage * 3
         print (((y+1), (y+3)))
         self.upperLimit = y+1
         self.lowerLimit = y+3
         data =  (self.db.getRange(self.conn, ((y+1), (y+3))))
         self.currentPage = self.currentPage + 1
         self.tableWidget.removeRow(0)
         self.tableWidget.removeRow(1)
         self.tableWidget.removeRow(2)
         self.tableWidget.removeRow(0)
         for count, row in enumerate(data):
             if count == 3:
                 return
             rowCount = self.tableWidget.rowCount()
             self.tableWidget.insertRow(rowCount)
             self.tableWidget.setRowHeight(rowCount, 75)
             for x in range(0, 4):
                 self.tableWidget.setItem(rowCount, x, QtWidgets.QTableWidgetItem(str(row[x])))

     def previousPage(self):
        if self.currentPage <= 0:
            print ("Lower limit page reached.")
            return

        y = self.currentPage * 3
        print (((y-2), (y)))
        self.upperLimit = y-2
        self.lowerLimit = y
        data =  (self.db.getRange(self.conn, ((y-2), (y))))
        self.currentPage = self.currentPage - 1
        self.num_label.setText(str(self.currentPage))
        self.tableWidget.removeRow(0)
        self.tableWidget.removeRow(1)
        self.tableWidget.removeRow(2)
        self.tableWidget.removeRow(0)
        for count, row in enumerate(data):
            if count == 3:
                return
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowCount)
            self.tableWidget.setRowHeight(rowCount, 75)
            for x in range(0, 4):
                self.tableWidget.setItem(rowCount, x, QtWidgets.QTableWidgetItem(str(row[x])))


     def rowSelect(self, row, col):
        print (row, col)
        self.selectedRow = row
        self.selectedColumn = col

     def makeTable(self):
        self.tableWidget.setColumnWidth(0,50)
        for x in range(1, 3):
            self.tableWidget.setColumnWidth(x, 315)

     def generateDialog(self, type):
                 self.addDialog.run()

     def addBook(self):
        self.generateDialog("Add")
        if self.addDialog.cancelled:
            self.addDialog.cancelled = False
            return
        if not (self.addDialog.author_edit.text() or self.addDialog.title_lineEdit.text() or self.addDialog.year_lineEdit.text()):
            return

        rowCount = self.tableWidget.rowCount()
        if not rowCount == 0:
            print ("Rows: " + str(rowCount))
            lastRowId = self.tableWidget.item(rowCount-1, 0).text()
        else: lastRowId = 0
        book = [
                 str( int(lastRowId) + 1 ),
                 str( self.addDialog.author_edit.text()    ),
                 str( self.addDialog.title_lineEdit.text() ),
                 str( self.addDialog.year_lineEdit.text()  )
               ]
        print (self.db.addBook(self.conn, (book[1], book[2], book[3])))
        if (self.tableWidget.rowCount() < 3):

            rowCount = self.tableWidget.rowCount()

            self.tableWidget.insertRow(rowCount)
            self.tableWidget.setRowHeight(rowCount, 75)
            for x in range(0, 4):
                self.tableWidget.setItem(rowCount, x, QtWidgets.QTableWidgetItem(str(book[x])))
        self.maxRows = self.db.getAll( self.conn )
        self.denom_label.setText(str(int(len(self.maxRows) / 3)))

     def editBook(self):
        print ("Edit book has been called.")


     def deleteBook(self):
         print ("Delete book has been called.")
         rowToBeDeleted =  (self.tableWidget.item(self.selectedRow, 0).text())
         self.db.deleteBook(self.conn, (str(rowToBeDeleted)))
         self.tableWidget.removeRow(self.selectedRow)
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
