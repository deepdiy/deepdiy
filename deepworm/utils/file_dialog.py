from tkinter import filedialog
from tkinter import *


def open_folder():
    root = Tk()
    root.withdraw()
    root.folder_name = filedialog.askdirectory()
    root.destroy()
    return root.folder_name

def open_file():
    root = Tk()
    root.withdraw()
    file_name =  filedialog.askopenfilename(initialdir = "/",title = "Select file")
    root.destroy()
    return file_name

def save_file():
    root = Tk()
    root.withdraw()
    file_name =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file")
    root.destroy()
    return (file_name)

if __name__ == '__main__':
    print(open_folder())
