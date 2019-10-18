from tkinter import *

class userGui:
    def __init__(self):
        window = Tk()

        def clicked():
            ServerIp = txt1.get()
            locoAddress = txt2.get() 

            if ((ServerIp != "") and (locoAddress != "")):
                print("gamer rage")
        
        window.title("Server IP and Locomotive Address")
        
        window.geometry('250x100')

        prompt1 = Label(window, text="Enter Server IP: ")
        prompt1.grid(column=1, row=1)

        prompt2 = Label(window, text="Enter Locomotive Address: ")
        prompt2.grid(column=1, row=2)
        
        txt1 = Entry(window,width=15)
        txt1.grid(column=2, row=1)

        txt2 = Entry(window,width=15)
        txt2.grid(column=2, row=2)
        
        btn = Button(window, text="Done", command=clicked) 
        btn.grid(column=1, row=3)

        window.mainloop()