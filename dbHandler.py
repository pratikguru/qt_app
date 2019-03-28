import json
import os

import sqlite3
from sqlite3 import Error


class DBHandler():
    def __init__(self, fileName):
        self.fileName = fileName

    def insertData(self,buffer):
        with open("db.txt", 'w+', encoding = "utf-8", ) as file:
            message = {}
            message = {
                "data" : buffer
            }
            file.write(json.dumps(message, indent=4))

    def retrieveData(self):
        data = (json.loads(open('db.txt', 'r').read()))
        return data

class DBSql():
    def __init__(self):
        self.name = "lowda"

    def create_connection(self, db):
        try:
            conn = sqlite3.connect(db)
            return conn
        except error as e:
            print (e)


    def create_table(self, conn, create_table_sql):
        try:
            c = conn.cursor()
            c.execute( create_table_sql )
        except Error as e:
            print (e)

    def addBook(self, conn, book):
        sql = """
                INSERT INTO BOOK (AUTHOR,TITLE,YEAR) VALUES(?,?,?)
                """
        cur = conn.cursor()
        print (cur.execute(sql, book))
        conn.commit()
        return cur.lastrowid

    def deleteBook(self, conn, id):
        sql = "DELETE FROM BOOK where rowid=?"
        cur = conn.cursor()
        cur.execute(sql, id)
        conn.commit()
        return cur.lastrowid

    def editAuthor(self, conn, edit):
        sql = """UPDATE BOOK
                 SET AUTHOR=?
                 WHERE rowid=?;"""
        cur = conn.cursor()
        cur.execute(sql, edit)
        conn.commit()
        return cur.lastrowid

    def editTitle(self, conn, edit):
        sql = """UPDATE BOOK
                 SET TITLE=?
                 WHERE rowid=?;"""
        cur = conn.cursor()
        cur.execute(sql, edit)
        conn.commit()

    def editYear(self, conn, edit):
        sql = """UPDATE BOOK
                 SET YEAR=?
                 WHERE rowid=?;"""
        cur = conn.cursor()
        cur.execute(sql, edit)
        conn.commit()

    def getAll(self, conn):
            sql = """
                    SELECT rowid,* FROM BOOK;
                  """
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return rows

    def getRange(self, conn, range):
        sql = """
                SELECT rowid,* from book where rowid between ? and ?;
              """
        cur = conn.cursor()
        cur.execute(sql, range)
        rows = cur.fetchall()
        return rows

    def filterByAuthor(self, conn, data):
        sql = """
                SELECT rowid,* FROM BOOK WHERE AUTHOR=?;
              """
        cur = conn.cursor()
        cur.execute(sql, data)
        rows = cur.fetchall()
        return rows

    def filterByTitle(self, conn, data):
        sql = """
                SELECT rowid,* FROM BOOK WHERE TITLE=?;
              """
        cur = conn.cursor()
        cur.execute(sql, data )
        rows = cur.fetchall()
        return rows

    def filterByYear(self, conn, data):
        sql = """
                SELECT rowid,* FROM BOOK WHERE YEAR=?;
              """
        cur = conn.cursor()
        cur.execute(sql, data)
        rows = cur.fetchall()
        return rows

    def getAllYears(self, conn):
        sql = """
                SELECT  YEAR FROM BOOK;
              """
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    def filterBookAT(self, conn, filter):
        sql = """
                SELECT rowid, * FROM BOOK WHERE AUTHOR=? AND TITLE=?;
              """
        cur = conn.cursor()
        cur.execute(sql, filter)
        rows = cur.fetchall()
        return rows

    def filterBookAY(self, conn, filter):
        sql = """
                SELECT rowid, * FROM BOOK WHERE AUTHOR=? AND YEAR=?;
              """
        cur = conn.cursor()
        cur.execute(sql, filter)
        rows = cur.fetchall()
        return rows

    def filterBookYT(self, conn, filter):
        sql = """
                SELECT rowid, * FROM BOOK WHERE YEAR=? AND TITLE=?;
              """
        cur = conn.cursor()
        cur.execute(sql, filter)
        rows = cur.fetchall()
        return rows

    def filterBook(self, conn, filter):
        sql = """
                SELECT rowid, * FROM BOOK WHERE AUTHOR=? and TITLE=? and YEAR=?;
              """
        cur = conn.cursor()
        cur.execute(sql, filter)
        rows = cur.fetchall()
        return rows

if __name__ == "__main__":

    db = DBSql()
    conn = db.create_connection("tester.db")
    book = """
            CREATE TABLE IF NOT EXISTS BOOK (
                AUTHOR TEXT NOT NULL,
                TITLE  TEXT NOT NULL,
                YEAR   INTEGER NOT NULL )
           """

    if conn is not None:
        #db.create_table(conn, book)
        print (db.addBook(conn, ("one", "two", 1198)))
        #print (db.getAll(conn))
        #print (db.filterByAuthor(conn, ("one",)))
        #print (db.filterByTitle(conn, ("shata",)))
        #print (db.filterByYear(conn, ("231",)))
        #print (db.getAllYears(conn))
        # rows = db.getRange(conn, (6, 8))
        # print (rows)
        # print (db.editAuthor(conn, ("bull", "2")))
        # print (db.editTitle(conn, ("tin tin", "2")))
        # print (db.editYear(conn, ("2002", "2")))
        #print (db.filterBook(conn, ("one", "shata", 1198)))
        #print (db.deleteBook(conn,("1")))
