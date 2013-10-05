#!/usr/bin/python2

import sys
import os
import sqlite3
from os import system

CURR_PATH, FILE_NAME = os.path.split(os.path.realpath(__file__))
CURR_PATH =     CURR_PATH + "//"
MN_CONTENT =    CURR_PATH + "mn_content"
MN_SKEL =       CURR_PATH + "mn_skel"
MN_CONKYRC =    CURR_PATH + "mn_conkyrc"
BIN_PUT_COMMENT_OFF =   CURR_PATH + "cmd.sh"
db_file =       CURR_PATH + "//" + "dbData.sq3"

def red(string):
    return ("\033[31m" + string + "\033[0m")

class   ConkyNotes():
    def __init__(self):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
#        print(list(self.getData()))

    def rmDb(self):
        self.request("DROP TABLE conkyNotes")

    def createDb(self, query):
        self.request(query)

    def resetDb(self, query = "CREATE TABLE conkyNotes (id INT, title TEXT, content TEXT)"):
        self.rmDb()
        self.createDb(query)
        self.request("INSERT INTO conkyNotes (id, title, content) VALUES (0, null, null)")

    def lastId(self):
        self.request("SELECT max(conkyNotes.id) FROM conkyNotes")
        for i in self.cur:
            return i[0]

    def dbAdd(self, title, content):
        self.request("INSERT INTO conkyNotes (id, title, content) VALUES ("+str(self.lastId() + 1)+", '"+title+"', '"+content+"')")

    def dbDel(self, id_):
        self.request("DELETE FROM conkyNotes WHERE id = " + str(id_))

    def request(self, request):
        self.cur.execute(request)
        self.conn.commit()

    def addNote(self, title, content):
        self.dbAdd(title, content)
        self.majConkyrc()

    def delNote(self):
        self.affData();
        while (1):
            try:
                toDel = input("Enter the note number you want to delete\n")
                toDel = int(toDel)
                break
            except:
                exit()
        if (toDel != 0):
            try:
                self.dbDel(self.data[toDel - 1][1])
            except:
                exit()
#        list(self.getData())[1])
        self.majConkyrc()

    def affData(self):
        """ Print datai """
        self.data = self.getData()
        i = 0
        while (i < len(self.data)):
            self.data[i] = list(self.data[i])
            self.data[i] = [(i + 1)] + self.data[i]
            i = i + 1
        for i in self.data:
            print(red(str(i[0])) +'.\t'+ i[2] + "\n" + i[3] + red("\n------------"))

    def getData(self):
        """ Get all data in BDD """
        self.cur.execute("SELECT * FROM conkyNotes WHERE conkyNotes.id != 0")
        self.conn.commit()
        return list(self.cur)

    def majConkyrc(self):
        """ Update the content of your conkyrc """
        data = self.getData()
        content = ""
        for i in data:
            content = content+ "${color #1992d6}" +i[1] + " ${hr 3}${color #ffffff}" + '\n' + i[2] + '\n'
#        print(content)
        f = open(MN_CONTENT, "w")
        f.write(content)
        f.close()
        # Met le contenu du skelette dans MN_CONKYRC
        #        system("cat " + CURR_PATH + MN_SKEL     + " > " +CURR_PATH  + MN_CONKYRC)
        system("sh " + BIN_PUT_COMMENT_OFF + " " + MN_SKEL + " > " + MN_CONKYRC)
        # Lui ajoute le contenu de la base de donnees
        system("cat " + MN_CONTENT  + " >> " + MN_CONKYRC)

    def __destroy__(self):
        """ Close the cursor and database connection """
        self.cur.close()
        self.conn.close()

cN = ConkyNotes()

if (len(sys.argv) == 4 and sys.argv[1] == "add"):
    cN.addNote(sys.argv[2], sys.argv[3])
    cN.majConkyrc()
elif (len(sys.argv) == 2 and sys.argv[1] == "del"):
    cN.delNote()
    cN.majConkyrc()
elif (len(sys.argv) == 2 and sys.argv[1] in ["help", "--help", "-h"]):
    print("Usage : \n\t- note add title content\n\t- note del\t\t: print all notes and ask you how note you want to delete\n\t- note\t\t\t: print all notes in console")
else:
    cN.affData()

cN.__destroy__()
