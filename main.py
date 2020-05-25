from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
alldata = []

#function to close form
def exit_but_main():
    mainWindow.destroy()

#functino to sort
def sort_but(thisData, form, entBox):
    #check did user enter column, if not use first column as default
    if entBox.get() in thisData.columns :
        col = entBox.get()
        form.delete(1.0, END)
        form.insert(END, thisData.sort_values(by = [col]))
    elif len(entBox.get()) == 0:
        col = thisData.columns[0]
    else:
        messagebox.showerror(title = "Error", message = "Unknown Column Name")

#function to cast string to number
def safe_cast(str):
    try:
        return int(str)
    except:
        return None

#function to select data
def select_but(thisData, form, low, high, entBox):
    #check if range text box is enter correctly
    if len(low.get()) == 0:
        lowRange = float("-inf")
    else:
        lowRange = safe_cast(low.get())
        if lowRange is None:
            messagebox.showerror(title = "Error", message = "Invalid Range")
            return

    if len(high.get()) == 0:
        highRange = float("inf")
    else:
        highRange = safe_cast(high.get())
        if highRange is None:
            messagebox.showerror(title = "Error", message = "Invalid Range")
            return

    #check did user enter column, if not use first column as default
    if entBox.get() in thisData.columns :
        col = entBox.get()
    elif len(entBox.get()) == 0:
        col = thisData.columns[0]
    else:
        messagebox.showerror(title = "Error", message = "Unknown Column Name")
        return

    #actual select data
    selectedData = thisData[col].between(lowRange,highRange, inclusive = False)
    form.delete(1.0, END)
    form.insert(END, thisData[selectedData])

#functino to show original data
def original_but(thisData, form):
    form.delete(1.0, END)
    form.insert(END, thisData)

#function for graph data
def graph_but(thisData,x,y,z,num):
    if num.get() == "All data":
        for col in thisData.columns:
            plt.scatter(thisData.index.array, thisData[col], label = col)
        plt.legend()
        plt.show()
        #for col in thisData.columns:
        #plt.show()

#thisData.index.array


    elif num.get() == "2 data":
        thisData.plot.scatter(x.get(), y.get())
        plt.show()
    elif num.get() == "3 data":
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        xAx = thisData[x.get()]
        yAx = thisData[y.get()]
        zAx = thisData[z.get()]
        ax.scatter(xAx, yAx, zAx, marker ='o')
        ax.set_xlabel(x.get())
        ax.set_ylabel(y.get())
        ax.set_zlabel(z.get())
        plt.show()

def model_but(thisData,x,y):

    xAx = thisData[x.get()]
    yAx = thisData[y.get()]
    fit = np.polyfit(xAx, yAx,1)
    fit_fn = np.poly1d(fit)
    plt.plot(xAx , yAx, 'yo', xAx, fit_fn(xAx), '--k')
    plt.xlim(xAx.min(), xAx.max())
    plt.ylim(yAx.min(), yAx.max())
    plt.show()

#initial windows to show data
def init_secondFrame(thisData):

    #create obejct
    secondWindow = Tk()
    secondWindow.geometry('800x400')
    secondWindow.title("Next")

    sortButton = Button(secondWindow, text= "Sort", command = lambda: sort_but(thisData, dataDisplay, sortCombo))
    selectButton = Button(secondWindow, text= "Select", command = lambda: select_but(thisData, dataDisplay, rangeLow, rangeHigh, sortCombo))
    graphButton = Button(secondWindow, text= "Graph", command = lambda: graph_but(thisData,xCombo,yCombo,zCombo,typeCombo))
    oriButton = Button(secondWindow, text= "Original", command = lambda: original_but(thisData, dataDisplay))
    modelButton = Button(secondWindow, text= "Model", command = lambda: model_but(thisData,xCombo,yCombo))

    sortLabel = Label(secondWindow, text = "Column", )
    selectLabel = Label(secondWindow, text = " < value < ")
    graphLabel = Label(secondWindow, text = "Type")

    xLabel = Label(secondWindow, text = "X:")
    yLabel = Label(secondWindow, text = "Y:")
    zLabel = Label(secondWindow, text = "Z:")


#    sortEnt = Entry(secondWindow, width = 6)
    rangeLow = Entry(secondWindow, width = 6)
    rangeHigh = Entry(secondWindow, width = 6)

    colName = []
    for col in thisData.columns:
        colName.append(col)
    sortCombo = ttk.Combobox(secondWindow, values = colName, width = 6)
    sortCombo.current(0)

    xCombo = ttk.Combobox(secondWindow, values = colName, width = 6)
    xCombo.current(0)
    yCombo = ttk.Combobox(secondWindow, values = colName, width = 6)
    yCombo.current(0)
    zCombo = ttk.Combobox(secondWindow, values = colName, width = 6)
    zCombo.current(0)

    typeCombo = ttk.Combobox(secondWindow, values = ["All data", "2 data", "3 data"], width = 8)
    typeCombo.current(0)

    dataDisplay = Text(secondWindow, width = 50)
    scrollBar = Scrollbar(secondWindow, orient='vertical', command = dataDisplay.yview)
    dataDisplay.configure(yscrollcommand = scrollBar.set)
    dataDisplay.insert(END, thisData)

    #locate object
    sortButton.grid(row = 1, column = 2, padx = 25, sticky = W)
    selectButton.grid(row = 2, column = 2, padx = 25, sticky = W)
    graphButton.grid(row = 3, column = 2, padx = 25, sticky = W)
    modelButton.grid(row = 4, column = 2, padx = 25, sticky = W)
    oriButton.grid(row = 5, column = 2, padx = 25, sticky = W)

    xLabel.grid(row = 3, column = 5, padx = 10)
    yLabel.grid(row = 4, column = 5, padx = 10)
    zLabel.grid(row = 5, column = 5, padx = 10)
    xCombo.grid(row = 3, column = 6)
    yCombo.grid(row = 4, column = 6)
    zCombo.grid(row = 5, column = 6)

    sortLabel.grid(row = 1, column = 3, columnspan = 3)
    sortCombo.grid(row = 1, column = 6, columnspan = 1)

    graphLabel.grid(row = 3, column = 3)
    typeCombo.grid(row = 3, column = 4)

    rangeLow.grid(row = 2, column = 3)
    selectLabel.grid(row = 2, column = 4, columnspan = 2)
    rangeHigh.grid(row = 2, column = 6)

    dataDisplay.grid(row = 0, column = 0, rowspan = 6)
    scrollBar.grid(row = 0, column = 1, rowspan = 6, sticky = NS)


#function to entry data file
def enter_but():

    #check is the textbox empty or not
    inputPath = entryMain.get()
    if len(inputPath) == 0:
        messagebox.showerror(title = "Error", message = "File path is empty")
        entryMain.text = ""
    else:

        #try to open file safely
        try:
            #if it is txt file
            if inputPath.find('.txt') != -1:
                with open(inputPath,"r") as file:
                    f = file.readlines()
                    empty = 0
                    arrData = []

                    #read data into array
                    for ln in f:
                        newLn = ln.strip("\n")
                        text = newLn.split(',')
                        arrData.append(text)
                        print(text)
                    file.close
                    alldata = pd.DataFrame(arrData)
                    init_secondFrame(alldata)

            #if it is csv file
            elif inputPath.find('csv') != -1:
                alldata = pd.read_csv(inputPath)
                init_secondFrame(alldata)

            #unknown file type
            else:
                messagebox.showerror(title = "Error", message = "Invalid file type")
                entryMain.text = ""

        except FileNotFoundError:
            messagebox.showerror(title = "Error", message = "Fail to open file")

#locate and create object
mainWindow = Tk()
mainWindow.geometry('300x200')
mainWindow.title("Main")

labelMain = Label(mainWindow, text= "Please Enter File Full Path")
entryMain = Entry(mainWindow)
buttonMain = Button(mainWindow, text= "Enter", command = enter_but)
exitButton = Button(mainWindow, text= "Exit", command = exit_but_main)

labelMain.pack(pady = 10)
entryMain.pack(pady = 10)
buttonMain.pack(pady = 10)
exitButton.pack(pady = 10)

mainWindow.mainloop()
