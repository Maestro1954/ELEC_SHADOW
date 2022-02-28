import tkinter

mygui = tkinter.Tk()

mygui.geometry('450x450+500+300')
mygui.title('my tkinter')

count = 0


def add():
    global count
    count += 1
    print(count)

def sub():
    global count
    count -= 1
    print(count)


button = tkinter.Button(text='add 1', command=add).pack()
button1 = tkinter.Button(text='sub 1', command=sub).pack()

mygui.mainloop()
