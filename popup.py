import json
import os



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


db = DBHandler("db.txt")
buffer = []
buffer.append({"book":"thuke", "title":"thika","year":1997})
buffer.append({"book":"apples", "title":"nice","year":2000})
db.insertData(buffer)
for x in (db.retrieveData()["data"]):
    print (x["book"], x["title"], x["year"])
