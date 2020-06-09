from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
all_data = []

#function to close form
def exit_but_main():
    main_window.destroy()

#function to sort
def sort_but(data, form, ent_Box):

    #check enter column, if not use first column as default, return error
    if ent_Box.get() in data.columns :
        col = ent_Box.get()
        form.delete(1.0, END)
        form.insert(END, data.sort_values(by = [col]))
    elif len(ent_Box.get()) == 0:
        col = data.columns[0]
    else:
        messagebox.showerror(title = "Error", message = "Unknown Column Name")

#function to cast string to number, return null if error
def safe_cast(str):
    try:
        return int(str)
    except:
        return None

#function to select data
def select_but(data, form, low, high, ent_Box):

    #if range enter box is empty use infinite, return error
    if len(low.get()) == 0:
        low_Range = float("-inf")
    else:
        low_Range = safe_cast(low.get())
        if low_Range is None:
            messagebox.showerror(title = "Error", message = "Invalid Range")
            return

    if len(high.get()) == 0:
        high_Range = float("inf")
    else:
        high_Range = safe_cast(high.get())
        if high_Range is None:
            messagebox.showerror(title = "Error", message = "Invalid Range")
            return

    #check did user enter column, if not use first column as default, return error
    if ent_Box.get() in data.columns :
        col = ent_Box.get()
    elif len(ent_Box.get()) == 0:
        col = data.columns[0]
    else:
        messagebox.showerror(title = "Error", message = "Unknown Column Name")
        return

    #remain the data being selected, and output
    selected_Data = data[col].between(low_Range,high_Range, inclusive = False)
    form.delete(1.0, END)
    form.insert(END, data[selected_Data])

#function to show original data
def original_but(data, form):
    form.delete(1.0, END)
    form.insert(END, data)

#function for graph data
def graph_but(data,x,y,z,num):
    #3 different mode, depend on how many data input
    if num.get() == "All data":
        for col in data.columns:
            plt.scatter(data.index.array, data[col], label = col)
        plt.legend()
        plt.show()
    elif num.get() == "2 data":
        data.plot.scatter(x.get(), y.get())
        plt.show()
    elif num.get() == "3 data":
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x_axis = data[x.get()]
        y_axis = data[y.get()]
        z_axis = data[z.get()]
        ax.scatter(x_axis, y_axis, z_axis, marker ='o')
        ax.set_xlabel(x.get())
        ax.set_ylabel(y.get())
        ax.set_zlabel(z.get())
        plt.show()

#function for create model require 2 column of data
def model_but(data,x,y):

    x_axis = data[x.get()]
    y_axis = data[y.get()]
    fit = np.polyfit(x_axis, y_axis,1)
    fit_fn = np.poly1d(fit)
    plt.plot(x_axis , y_axis, 'yo', x_axis, fit_fn(x_axis), '--k')
    plt.xlim(x_axis.min(), x_axis.max())
    plt.ylim(y_axis.min(), y_axis.max())
    plt.show()

#initial windows to show data
def init_secondFrame(thisData):

    #create obejct
    second_window = Tk()
    second_window.geometry('800x400')
    second_window.title("Next")

    col_name = []
    for col in thisData.columns:
        col_name.append(col)
    sort_combo = ttk.Combobox(second_window, values = col_name, width = 6)
    sort_combo.current(0)
    x_combo = ttk.Combobox(second_window, values = col_name, width = 6)
    x_combo.current(0)
    y_combo = ttk.Combobox(second_window, values = col_name, width = 6)
    y_combo.current(0)
    z_combo = ttk.Combobox(second_window, values = col_name, width = 6)
    z_combo.current(0)
    type_combo = ttk.Combobox(second_window, values = ["All data", "2 data", "3 data"], width = 8)
    type_combo.current(0)

    #give function to object
    sort_button = Button(second_window, text= "Sort", command = lambda: sort_but(thisData, data_display, sort_combo))
    select_button = Button(second_window, text= "Select", command = lambda: select_but(thisData, data_display, range_low, range_high, sort_combo))
    graph_button = Button(second_window, text= "Graph", command = lambda: graph_but(thisData,x_combo,y_combo,z_combo,type_combo))
    ori_button = Button(second_window, text= "Original", command = lambda: original_but(thisData, data_display))
    model_button = Button(second_window, text= "Model", command = lambda: model_but(thisData,x_combo,y_combo))

    #init label, enter box
    sort_label = Label(second_window, text = "Column", )
    select_label = Label(second_window, text = " < value < ")
    graph_label = Label(second_window, text = "Type")

    x_label = Label(second_window, text = "X:")
    y_label = Label(second_window, text = "Y:")
    z_label = Label(second_window, text = "Z:")


    range_low = Entry(second_window, width = 6)
    range_high = Entry(second_window, width = 6)


    #setup data display scroll bar
    data_display = Text(second_window, width = 50)
    scroll_bar = Scrollbar(second_window, orient='vertical', command = data_display.yview)
    data_display.configure(yscrollcommand = scroll_bar.set)
    data_display.insert(END, thisData)

    #locate object
    sort_button.grid(row = 1, column = 2, padx = 25, sticky = W)
    select_button.grid(row = 2, column = 2, padx = 25, sticky = W)
    graph_button.grid(row = 3, column = 2, padx = 25, sticky = W)
    model_button.grid(row = 4, column = 2, padx = 25, sticky = W)
    ori_button.grid(row = 5, column = 2, padx = 25, sticky = W)

    x_label.grid(row = 3, column = 5, padx = 10)
    y_label.grid(row = 4, column = 5, padx = 10)
    z_label.grid(row = 5, column = 5, padx = 10)
    x_combo.grid(row = 3, column = 6)
    y_combo.grid(row = 4, column = 6)
    z_combo.grid(row = 5, column = 6)

    sort_label.grid(row = 1, column = 3, columnspan = 3)
    sort_combo.grid(row = 1, column = 6, columnspan = 1)

    graph_label.grid(row = 3, column = 3)
    type_combo.grid(row = 3, column = 4)

    range_low.grid(row = 2, column = 3)
    select_label.grid(row = 2, column = 4, columnspan = 2)
    range_high.grid(row = 2, column = 6)

    data_display.grid(row = 0, column = 0, rowspan = 6)
    scroll_bar.grid(row = 0, column = 1, rowspan = 6, sticky = NS)


#function to entry data file
def enter_but():

    #check is the textbox empty or not, throw error message if file is empty
    input_path = entry_main.get()
    if len(input_path) == 0:
        messagebox.showerror(title = "Error", message = "File path is empty")
        entry_main.text = ""
    else:
        #try to open file safely
        try:
            #if it is csv file
            if input_path.find('csv') != -1:
                all_data = pd.read_csv(input_path)
                init_secondFrame(all_data)
                print(all_data.columns)
            #unknown file type
            else:
                messagebox.showerror(title = "Error", message = "Invalid file type")
                entry_main.text = ""

        except FileNotFoundError:
            messagebox.showerror(title = "Error", message = "Fail to open file")

#locate and create object
main_window = Tk()
main_window.geometry('300x200')
main_window.title("Main")

label_main = Label(main_window, text= "Please Enter File Full Path")
entry_main = Entry(main_window)
button_main = Button(main_window, text= "Enter", command = enter_but)
exit_button = Button(main_window, text= "Exit", command = exit_but_main)

label_main.pack(pady = 10)
entry_main.pack(pady = 10)
button_main.pack(pady = 10)
exit_button.pack(pady = 10)

main_window.mainloop()
