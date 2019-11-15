# To display a gui to the user to get easy input
# Created by: Jared Wagler
# Updated on: 11/15/2019

from tkinter import *
import os

class userGui:
    def __init__(self):

        self.serverIp = ""                                          # initialize the IP as blank to start
        self.locoAddress = ""                                       # initialize the locomotive address as blank to start
        ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))    # gets the root folder the program is in
        INFO = os.path.join(ROOT_FOLDER, 'info.txt')                # grabs the info file for us

        window = Tk()

        def manualClicked():            # user clicked manual input
            global serverIp
            global locoAddress
            serverIp = txt1.get()       # grabs IP from prompt
            locoAddress = txt2.get()    # grabs locomotive address from prompt
            f = open(INFO,'w')          # opens info file in write mode
            f.write(serverIp + '\n')    # writes user input into the file
            f.write(locoAddress)

            if ((serverIp != "") and (locoAddress != "")):  # only closes gui if user entered info
                f.close()
                window.destroy()
        
        def fileClicked():                          # user clicked previous input
            global serverIp
            global locoAddress
            f = open(INFO,'r')                      # opens info file in read mode
            serverIp = f.readline()                 # grabs IP from file
            serverIp = serverIp.rstrip('\n')
            locoAddress = f.readline()              # grabs locomotive address from file
            locoAddress = locoAddress.rstrip('\n')
            f.close()
            window.destroy()
        
        window.title("Enter IP and Address")
        
        window.geometry('310x130')

        prompt1 = Label(window, text="Enter Server IP: ")                   # IP prompt
        prompt1.grid(column=1, row=1)

        prompt2 = Label(window, text="Enter Locomotive Address: ")          # locomotive address prompt
        prompt2.grid(column=1, row=2)
        
        txt1 = Entry(window,width=15)                                       # text entry for IP
        txt1.grid(column=2, row=1)
        txt1.focus_set()                                                    # sets cursor to start at this prompt

        txt2 = Entry(window,width=15)                                       # text entry for locomotive address
        txt2.grid(column=2, row=2)
        
        btn1 = Button(window, text="Manual Input", command=manualClicked)   # manual input button
        btn1.grid(column=2, row=3)

        btn2 = Button(window, text="Previous Input", command=fileClicked)   # file input button
        btn2.grid(column=1, row=3)

        f = open(INFO,'r')              # opens info file in read mode
        tempIP = f.readline()           # gets previous IP to display on gui
        tempIP= tempIP.rstrip('\n')
        tempAdr = f.readline()          # gets previous locomotive address to display on gui
        tempAdr = tempAdr.rstrip('\n')

        lastIP = Label(window, text="Previous IP Address: " + tempIP)           # displays previously used IP address
        lastIP.grid(column=1, row=4, pady=(10,0))

        lastAdr = Label(window, text="Previous Locomotive Address: " + tempAdr) # displays previously used locomotive address
        lastAdr.grid(column=1, row=5)

        window.mainloop()

    def returnValues(self):             # returns IP and locomotive address to main part of code
        global serverIp
        global locoAddress
        return serverIp, locoAddress

# for testing the gui without having to open readSensor.py
# guiInput = userGui()
