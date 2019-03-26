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
                INSERT INTO BOOK(BOOK_ID, AUTHOR, TITLE, YEAR)
                VALUES(?,?,?,?)
                """
        cur = conn.cursor()
        cur.execute(sql, book)
        return cur.lastrowid

if __name__ == "__main__":
    # db = DBHandler("db.txt")
    # buffer = []
    # buffer.append({"author":"thuke", "title":"thika","year":1997})
    # buffer.append({"author":"apples", "title":"nice","year":2000})
    # db.insertData(buffer)
    # for x in (db.retrieveData()["data"]):
    #     print (x["author"], x["title"], x["year"])
    db = DBSql()
    conn = db.create_connection("tester.db")
    book = """
                CREATE TABLE IF NOT EXISTS BOOK (
                    BOOK_ID INTEGER BOOK ID,
                    AUTHOR TEXT NOT NULL,
                    TITLE  TEXT NOT NULL,
                    YEAR   INTEGER NOT NULL,
                    PRIMARY KEY (BOOK_ID)
                );
           """
    if conn is not None:
        db.create_table(conn, book)
        print (db.addBook(conn, (2, "tintin", "maga", 1998)))
