"""
The purpose of this script is to create a PyQt GUI that simulates the functionality of a
library.

@author: Pratik Gurudatt
@date  : 26/03/2019
"""
import copy
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
import math



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


    def runAdd(self):

        self.addButton.clicked.connect(self.addBookEmitSignal)
        self.cancelButton.clicked.connect(self.cancelBookEmitSignal)
        self.miniDialog.exec_()

    def runEdit(self):
        self.addButton.clicked.connect(self.editBookEmitSignal)
        self.cancelButton.clicked.connect(self.cancelBookEmitSignal)
        self.miniDialog.exec_()

    def editBookEmitSignal(self):
        self.miniDialog.close()

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
        #self.db             = DBHandler("db.txt") // Text based database.
        self.db             = DBSql()
        self.rowCount       = 0
        self.selectedRow    = None
        self.selectedColumn = None
        self.pageCount      = 0
        self.currentPage    = 0
        self.addDialog      = BookDialog("Add Book", "Add")
        self.editDialog     = BookDialog("Edit Book", "Edit")
        self.maxRows        = 0
        self.currentRow     = 0
        self.lowerLimit     = 1
        self.upperLimit     = 4
        self.filterMode     = False
        self.filteredResults = []
        self.makeTable()


        #Database connection initialization.
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
        """ Brief
            > Fill Combo box.
            > Add all data.
            > Set Labels.
        """
        years = self.db.getAllYears(self.conn)
        years = set(years)
        for year in years:
            self.year_select.addItem( str(year[0]) )

        books = []
        self.maxRows = self.db.getAll(self.conn)
        self.denom_label.setText(str(int(len(self.maxRows) / 3) ))

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
         """
            Function for capturing signals emitted by all the input fields of the form.
         """
         self.add_button.clicked.connect(self.addBook)
         self.edit_button.clicked.connect(self.editBook)
         self.delete_button.clicked.connect(self.deleteBook)
         self.filter_button.clicked.connect(self.filterBooks)
         self.clear_button.clicked.connect(self.clearFilter)
         self.tableWidget.cellClicked.connect(self.rowSelect)
         self.previous_button.clicked.connect(self.previousPage)
         self.next_button.clicked.connect(self.nextPage)
         self.tableWidget.cellDoubleClicked.connect(self.editBook)

     def nextPage(self):
         """
            Function for handling the next page functionality.

            On click of the next page, the current page attr is incremented.
            Based on the current page the slice of elements from the db are extracted.
            The sliced elements are fed into the table.
            Limits: (y+1), (y+3)
            The modes are checked before slicing. Incase of normal mode the above slicing is used.
            In case of filtering mode, the elements are sliced based on a linear array of 3 sets each.
         """
         if self.currentPage >= int(len(self.maxRows)/3):
             print ("Upper limit pages reached.")
             return
         self.currentPage = self.currentPage + 1
         self.num_label.setText(str(self.currentPage + 1))

         print (self.currentPage)
         y = int(self.currentPage * 3)
         print ("next range")
         print ((y+1), (y+3))
         data = None
         if self.filterMode:
            print( "FILTER MODE" )
            fdata = self.filteredResults
            sets = []
            i = 0
            for item in fdata:
                if i == 0:
                    sets.append( [] )
                sets[-1].append(item)
                i = (i + 1) % 3
            if self.currentPage < len(sets):
                data = sets[self.currentPage]
            else:
                data = []
         else:
             data =  (self.db.getRange(self.conn, ((y+1), (y+3))))
             print ("NORMAL MODE")
         print( "currentPage: " + str(self.currentPage))
         print( "data: " + str(data) )
         self.clearTable()
         for count, row in enumerate(data):
             if count == 3:
                 return
             rowCount = self.tableWidget.rowCount()
             self.tableWidget.insertRow(rowCount)
             self.tableWidget.setRowHeight(rowCount, 75)
             for x in range(0, len(row)):
                 self.tableWidget.setItem(count, x, QtWidgets.QTableWidgetItem(str(row[x])))


     def previousPage(self):
        """
        A function meant for handling previous button clicks.

        The function listens for previous button clicks, and decrements the page counter.
        The current page number is used to slice the data from the database.
        The sliced data is fed into the datatable.
        The data is sliced based on the mode of the form as stated in nextPage() function.
        """
        if self.currentPage == 0:
            print ("Lower limit page reached.")
            return
        print (self.currentPage)
        y = self.currentPage * 3
        self.num_label.setText(str(self.currentPage))
        self.currentPage = self.currentPage - 1
        print ("Previous range")


        data = None
        if self.filterMode:
            print( "FILTER MODE" )
            fdata = self.filteredResults
            sets = []
            i = 0
            for item in fdata:
                if i == 0:
                    sets.append( [] )
                sets[-1].append(item)
                i = (i + 1) % 3
            if self.currentPage < len(sets):
                data = sets[self.currentPage]
            else:
                data = []
        else:
            data =  (self.db.getRange(self.conn, ((y-2), (y))))
            print ((y-2), (y))
        print( "currentPage: " + str(self.currentPage))
        print( "data: " + str(data) )
        #
        #

        self.clearTable()
        for count, row in enumerate(data):
            if count == 3:
                return
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowCount)
            self.tableWidget.setRowHeight(rowCount, 75)
            for x in range(0, len(row)):
                self.tableWidget.setItem(rowCount, x, QtWidgets.QTableWidgetItem(str(row[x])))

     def clearTable(self):
         """
            A function meant for clearing the table widget.
         """
         self.tableWidget.removeRow(0)
         self.tableWidget.removeRow(1)
         self.tableWidget.removeRow(2)
         self.tableWidget.removeRow(0)

     def rowSelect(self, row, col):
        """
        A function meant for setting the selected row and selected column. (Cell)
        """
        print (row, col)
        self.selectedRow = row
        self.selectedColumn = col

     def makeTable(self):
        """
        A function meant for making the table with default settings.
        """
        self.tableWidget.setColumnWidth(0,50)
        for x in range(1, 3):
            self.tableWidget.setColumnWidth(x, 315)

     def generateDialog(self, type):
        """
        A function meant for generating the dialog based on the type.
        """
        if type == "Add":
            self.addDialog.runAdd()
        elif type == "Edit":
            self.editDialog.runEdit()



     def addBook(self):
        """
        A function meant for adding books to the db and the table.

        The function logically adds data to the table and db, the new data
        has to be fed through an edit box. The saved data is then written
        to the db.

        The current row count is taken into account, and if there are rows
        left (<3) the rows are added instantly.

        A complex logic is implemented to add the rows to the table while the
        above condition holds good.
        """
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
        self.year_select.clear()
        self.year_select.addItem("-")
        for year in self.db.getAllYears(self.conn):
            self.year_select.addItem(str(year[0]))

     def editBook(self):
        print ("Edit book has been called.")
        self.generateDialog("Edit")
        if self.editDialog.cancelled:
            self.editDialog.cancelled = False
            return
        if not (self.editDialog.author_edit.text() or self.editDialog.title_lineEdit.text() or self.editDialog.year_lineEdit.text()):
            return
        rowId =  (self.tableWidget.item(self.selectedRow, 0).text())
        book = [
            str(rowId),
            str( self.editDialog.author_edit.text()    ),
            str( self.editDialog.title_lineEdit.text() ),
            str( self.editDialog.year_lineEdit.text()  )
        ]
        if self.editDialog.author_edit.text():
            self.db.editAuthor(self.conn, (str(self.editDialog.author_edit.text()), str(rowId)))
            self.tableWidget.setItem(self.selectedRow, 1, QtWidgets.QTableWidgetItem(str(self.editDialog.author_edit.text())))

        if self.editDialog.title_lineEdit.text():
            self.db.editTitle(self.conn, (str(self.editDialog.title_lineEdit.text()), str(rowId)))
            self.tableWidget.setItem(self.selectedRow, 2, QtWidgets.QTableWidgetItem(str(self.editDialog.title_lineEdit.text())))

        if self.editDialog.year_lineEdit.text():
            self.db.editYear(self.conn, (str(self.editDialog.year_lineEdit.text()), str(rowId)))
            self.tableWidget.setItem(self.selectedRow, 3, QtWidgets.QTableWidgetItem(str(self.editDialog.year_lineEdit.text())))

     def deleteBook(self):
         print ("Delete book has been called.")
         if self.selectedRow is None:
             print ("Please select something...")
             return
         rowToBeDeleted =  (self.tableWidget.item(self.selectedRow, 0).text())

         print (rowToBeDeleted)
         self.db.deleteBook(self.conn, (str(rowToBeDeleted),))
         self.tableWidget.removeRow(self.selectedRow)
         self.maxRows = self.db.getAll(self.conn)
         self.selectedRow = None
         self.selectedColumn = None

     def filterBooks(self):
         self.filterMode = True
         self.currentPage = 0
         print ("Filter book has been called.")
         self.filteredResults = []

         data = None
         if len(self.author_edit.text()) > 1 and len(self.title_edit.text()) > 1 and self.year_select.currentText() != "-":
             print ("All Filters applied.")
             data = self.db.filterBook(self.conn, (self.author_edit.text(), self.title_edit.text(), self.year_select.currentText()))
         elif len(self.author_edit.text()) > 1  and len(self.title_edit.text()) > 1:
             print("Author title filter.")
             data = self.db.filterBookAT(self.conn, (self.author_edit.text(), self.title_edit.text()))
         elif len(self.author_edit.text()) > 1 and (self.year_select.currentText() != "-"):
             print ("Author year filter.")
             data = self.db.filterBookAY(self.conn, (self.author_edit.text(), self.year_select.currentText()))
         elif len(self.title_edit.text()) > 1 and self.year_select.currentText() != "-":
             print ("Title year filter.")
             data = self.db.filterBookYT(self.conn, (self.title_edit.text(), self.year_select.currentText()))
         elif len(self.title_edit.text()) > 1 :
             print ("Title Filter only.")
             data = self.db.filterByTitle(self.conn, (self.title_edit.text(), ))
         elif (self.year_select.currentText() != "-"):
             print ("Year Filter only.")
             data = self.db.filterByYear(self.conn, (self.year_select.currentText(), ))
         elif len(self.author_edit.text()) > 1:
             print ("Author Filter only.")
             data = self.db.filterByAuthor(self.conn, (self.author_edit.text(), ))
         if data is None:
             return
         self.filteredResults = data
         self.maxRows = data
         print (data)
         self.denom_label.setText(str(math.floor(len(self.maxRows)/3)))
         self.clearTable()
         for count, row in enumerate(data):
             if count == 3:
                 return
             rowCount = self.tableWidget.rowCount()
             self.tableWidget.insertRow(rowCount)
             self.tableWidget.setRowHeight(rowCount, 75)
             for x in range(0, 4):
                 self.tableWidget.setItem(rowCount, x, QtWidgets.QTableWidgetItem(str(row[x])))

     def clearFilter(self):
         self.filterMode = False
         print ("Clear filter has been called.")
         self.author_edit.clear()
         self.title_edit.clear()
         self.maxRows = self.db.getAll(self.conn)
         self.denom_label.setText(str(math.floor(len(self.maxRows)/3)))
         self.currentPage = 0
def main():
    app = QApplication(sys.argv)
    widget = App()
    widget.show()
    widget.run()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
