import tkinter as tk

def Clickedbutton1():
    print("button clicked")
    root.after(3000, root.destroy)

def Clickedbutton2():
    print("button clicked")
    root.after(5000, root.destroy)

root = tk.Tk()

root.title("My First Python Window") 
root.geometry("400x300")           

label = tk.Label(root, text="Hello, Tkinter!")
label.pack() 

my_button = tk.Button(root, text="Close Windows in 3", command=Clickedbutton1, padx=10, pady=5)

another_button = tk.Button(root, text="close windows in 5", command=Clickedbutton2, padx=100, pady=5)

another_button.pack(pady=50)

my_button.pack(pady=50)

root.mainloop()