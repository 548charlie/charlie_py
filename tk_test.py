from tkinter import *

class MyApp:
    def __init__(self, myParent):
        self.container = Frame(myParent)
        self.container.pack()

        self.button1 = Button(self.container)
        self.button1["text"] = "Hello World"
        self.button1["background"] = "green"
        self.button1.pack(side=LEFT)

        self.button2 = Button(self.container)
        self.button2.configure(text="Off to Join the circus")
        self.button2.configure(background="tan")
        self.button2.pack(side=LEFT)

        self.button3 = Button(self.container)
        self.button3.configure(text="Join me?", background="cyan")
        self.button3.pack(side=LEFT)

        self.button4 = Button(self.container, text="Good Bye!", background="red")
        self.button4.pack(side=LEFT) 

class MyApp2:
    def __init__(self, parent):
        self.myParent = parent
        self.container = Frame(parent)
        self.container.pack()
        
        self.button1 = Button(self.container)
        self.button1.configure(text="OK", background="green")
        self.button1.pack(side=LEFT)
        self.button1.focus_force() 
        self.button1.bind("<Button-1>", self.button1Click)
        self.button1.bind("<Return>", self.button1Click)

        self.button2 = Button(self.container)
        self.button2.configure(text="Cancel", background="red")
        self.button2.pack(side=LEFT)
        self.button2.bind("<Button-1>", self.button2Click)
        self.button2.bind("<Return>", self.button2Click)

    def button1Click(self, event):
        self.report_event(event) 
        if self.button1["background"] == "green":
            self.button1["background"] = "yellow"
        else:
            self.button1["background"] = "green"
    def button2Click(self, event):
        self.report_event(event) 
        self.myParent.destroy() 

    def report_event(self, event):
        event_name = {"2": "KeyPress", "4": "ButtonPress"}
        print("Time:" + str(event.time) + event_name[str(event.type) ] + "EventWidgetId=" + str(event.widget) + "EventKeySymbol " + str(event.keysym)  ) 
        
class MyApp3:
    def __init__(self, parent):
        self.myParent = parent
        self.container = Frame(parent)
        self.container.pack()
        
        self.button1 = Button(self.container, command=self.button1Click)
        self.button1.configure(text="OK", background="green")
        self.button1.pack(side=LEFT)
        self.button1.focus_force() 

        self.button2 = Button(self.container,command=self.button2Click)
        self.button2.configure(text="Cancel", background="red")
        self.button2.pack(side=RIGHT)

    def button1Click(self):
        print("button1Click event handler") 
        if self.button1["background"] == "green":
            self.button1["background"] = "yellow"
        else:
            self.button1["background"] = "green"
    def button2Click(self):
        print("button2Click event handler") 
        self.myParent.destroy() 

    def report_event(self, event):
        event_name = {"2": "KeyPress", "4": "ButtonPress"}
        print("Time:" + str(event.time) + event_name[str(event.type) ] + "EventWidgetId=" + str(event.widget) + "EventKeySymbol " + str(event.keysym)  ) 


root = Tk()
myapp = MyApp3(root)
root.mainloop() 

