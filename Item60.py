from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import shutil
import os
import datetime
import sqlite3
import time

conn = sqlite3.connect('drill.db')
c = conn.cursor()
sql = "SELECT * FROM accessTimes ORDER BY ID DESC LIMIT 1"


def tableCreate():
    c.execute("CREATE TABLE IF NOT EXISTS accessTimes(ID INTEGER PRIMARY KEY AUTOINCREMENT, datestamp TEXT)")

tableCreate()

def readData():
    for row in c.execute(sql):
            return row[1]
    

class Feedback:

    def __init__(self, master):

        master.title('File Selector')

        self.style = ttk.Style()

        #creating top frame
        self.frame_top = ttk.Frame(master)
        self.frame_top.pack()

        ttk.Label(self.frame_top, text = "Select Source File:").grid(row = 0, column = 0, sticky = 'w')
        ttk.Label(self.frame_top, text = "Select Destination File:").grid(row = 1, column = 0, sticky = 'w')
        ttk.Label(self.frame_top, text = "The last file transfer was made on: " + str(readData())).grid(row = 2, column = 0, columnspan = 2, sticky = 'w')

        self.entry_source = ttk.Entry(self.frame_top, width = 25)
        self.entry_destination = ttk.Entry(self.frame_top, width = 25)

        self.entry_source.grid(row = 0, column = 1, columnspan = 2, pady = 10)
        self.entry_destination.grid(row = 1, column = 1, columnspan = 2, pady = 10)

        ttk.Button(self.frame_top, text = 'Browse...', command = self.openFileSource).grid(row = 0, column = 3)
        ttk.Button(self.frame_top, text = 'Browse...', command = self.openFileDest).grid(row = 1, column = 3)

        #creating bottom frame
        self.frame_bottom = ttk.Frame(master)
        self.frame_bottom.pack()

        ttk.Button(self.frame_bottom, text = 'Submit', command = self.submit).grid(row = 0, column = 0, padx = 20, pady = 5)
        ttk.Button(self.frame_bottom, text = 'Clear', command = self.clear).grid(row = 0, column = 1, padx = 20, pady = 5)

    def openFileSource(self):
        name = filedialog.askdirectory(initialdir = "/Users/ExecutiveAssistant/Desktop/", title = 'Select a folder')
        self.entry_source.insert(0, name)

    def openFileDest(self):
        name = filedialog.askdirectory(initialdir = "/Users/ExecutiveAssistant/Desktop/", title = 'Select a folder')
        self.entry_destination.insert(0, name)

    def submit(self):
        source = (self.entry_source.get() + '/')
        dest = (self.entry_destination.get() + '/')
        date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))

        count = 0
        for files in os.listdir(source):
            if files.endswith('.txt'):
               unixts = os.path.getmtime(source + files)
               value = datetime.datetime.fromtimestamp(unixts)
               local = datetime.datetime.now()
               diff = (local - value).total_seconds()
               if diff < 86400:
                   shutil.move(source + files, dest)
                   count = count + 1
        messagebox.showinfo(title = "Important Message", message = str(count) + " files moved successfully!")
        c.execute("INSERT INTO accessTimes (datestamp) VALUES (?)",
              (date,))
        conn.commit()
        readData()

    def clear(self):
        self.entry_source.delete(0, 'end')
        self.entry_destination.delete(0, 'end')

def main():

    root = Tk()
    feedback = Feedback(root)
    root.mainloop()
    readData()

if __name__ == "__main__": main()
