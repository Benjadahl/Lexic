#!/usr/bin/python3

import sqlite3
import sys
from time import sleep, time
import ctypes as ct
from ctypes.util import find_library
from pykeylogger import keylogger
import time

con = None
cursor = None

#Sorry, but I depend on X11 at the moment. 
assert("linux" in sys.platform)

def initiateDB(fileName):
    try:
        con = sqlite3.connect(fileName)
    except sqlite3.Error:
        raise Exception("Could not connect to database")

def getWords(PrevWord):
    con = sqlite3.connect(sys.argv[1])
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Completions WHERE PrevWord=? ORDER BY Weight DESC", (PrevWord,))
    return cursor

initiateDB(sys.argv[1])

def cliLoop():
    #Hold on to your butts
    while True:
        textInput = input("Enter previous word: ")
        words = getWords(textInput)
        a = 0
        while a < 10:
            row = words.fetchone()
    
            if row == None:
                break
            
            print(row[1])
            a+=1

#cliLoop()
