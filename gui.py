import threading
from tkinter import *
from tkinter import font
from tkinter import ttk
import chat
import time

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()
        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width = False, height = False)
        self.login.configure(width = 180, height = 100)

        self.labelName = Label(self.login, text = "Username: ")
        self.labelPass = Label(self.login, text = "Password: ")
        self.labelName.place(relheight = 0.1, relx = 0, rely = 0.09)
        self.labelPass.place(relheight = 0.1, relx = 0, rely = 0.30)

        self.entryName = Entry(self.login)
        self.entryPass = Entry(self.login)
        self.entryName.place(relwidth = 0.5, relheight = 0.2, relx = 0.4, rely = 0.04)
        self.entryPass.place(relwidth = 0.5, relheight = 0.2, relx = 0.4, rely = 0.30)
        self.entryName.focus()
        self.go = Button(self.login, text = "CONTINUE", command = lambda: self.goAhead(self.entryName.get(), self.entryPass.get()))
        self.go.place(relx = 0, rely = 0.6, relwidth = 1, relheight = 0.3)
        self.Window.mainloop()

    def goAhead(self, name, passw):
        #print(name+"\n"+passw)
        chat.login(name, passw)
        t = threading.Thread(target=self.receive)
        t.start()
        self.layout(name)
        self.login.destroy()

    def layout(self,name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False, height = False)
        self.Window.configure(width = 470, height = 550, bg = "#101010")
        self.labelHead = Label(self.Window,
                             bg = "#17202A",
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
        self.textCons = Text(self.Window,
                             width = 20,
                             height = 2,
                             bg = "#17202A",
                             padx = 5,
                             pady = 5)

        self.textCons.place(relheight = 0.745,
                            relwidth = 1,
                            rely = 0.08)

        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)

        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold",
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06,
                             relwidth = 0.22)

        self.textCons.config(cursor = "arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)

        scrollbar.config(command = self.textCons.yview)

        self.textCons.config(state = DISABLED)

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.msg=msg
        self.entryMsg.delete(0, END)
        snd= threading.Thread(target = self.sendMessage)
        snd.start()

    def receive(self):
        time.sleep(1)
        self.textCons.tag_config("user", foreground="red")
        count = 0
        while(True):
            try:
                msgs = chat.getmsgs()
                if(msgs!=[]):
                    for a in msgs:
                        self.textCons.config(state = NORMAL)
                        self.textCons.insert(END, a["user"]+": "+a["text"]+"\n\n")
                        unlen = len(a["user"])
                        self.textCons.tag_add("user", "2.8", "1.13")#f"{count}.0", f"{count}.{unlen}")
                        count += 2
                        self.textCons.config(state = DISABLED)
                        self.textCons.see(END)
                time.sleep(3)
            except:
                print("error in receive")

    def sendMessage(self):
        chat.sendmsg(self.msg)

g = GUI()
