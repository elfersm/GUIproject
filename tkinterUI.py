from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import shutil
import os
import datetime

class Feedback:

    def __init__(self, master):

        master.title('File Selector')
        master.configure(background = '#faece9')

        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#faece9')

        #creating top frame
        self.frame_top = ttk.Frame(master)
        self.frame_top.pack()

        ttk.Label(self.frame_top, text = "Select Source File:").grid(row = 0, column = 0, sticky = 'w')
        ttk.Label(self.frame_top, text = "Select Destination File:").grid(row = 1, column = 0, sticky = 'w')

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
        messagebox.showinfo(title = "Important Message", message = str(count) + " files were moved successfully!")

    def clear(self):
        self.entry_source.delete(0, 'end')
        self.entry_destination.delete(0, 'end')

def main():

    root = Tk()
    feedback = Feedback(root)
    root.mainloop()

if __name__ == "__main__": main()
