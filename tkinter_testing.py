from tkinter import *


class Buttons:
    def __init__(self, master, prompt='Click Me', response='Click the Button', baby_button=None):
        self.frame = Frame(master)
        self.frame.pack()
        self.prompt = StringVar()
        self.prompt.set(prompt)
        self.response = StringVar()
        self.response.set(response)
        self.baby = baby_button
        self.button = Button(self.frame, textvariable=self.prompt, command=self.button_handler, fg="blue")
        self.button.pack(side=TOP)
        self.label = Label(self.frame, textvariable=self.response)
        self.label.pack(side=BOTTOM)
        self.click_count = 0

    def button_handler(self):
        self.click_count += 1
        self.baby.response.set("Click me not that one!")
        self.baby.prompt.set("Come on!")
        self.prompt.set("Click me again!")
        self.response.set("Keep clicking!")


root = Tk()

button = Buttons(root)
otherButton = Buttons(root, baby_button=button)
button.baby = otherButton

root.mainloop()
