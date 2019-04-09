from tkinter import filedialog
from tkinter import *


def select_folder():
    root = Tk()
    root.withdraw()
    root.folder_path = filedialog.askdirectory()
    root.destroy()
    return root.folder_path

def select_file():
    root = Tk()
    root.withdraw()
    file_path =  filedialog.askopenfilename(initialdir = "/",title = "Select file")
    root.destroy()
    return file_path

def select_save_path():
    root = Tk()
    root.withdraw()
    save_path =  filedialog.asksaveasfilepath(initialdir = "/",title = "Select file")
    root.destroy()
    return (save_path)

if __name__ == '__main__':
    print(select_folder())
