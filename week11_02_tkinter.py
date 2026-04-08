import tkinter as tk
from tkinter import messagebox

def on_click():
    messagebox.showinfo("Information", "Button clicked!")

root = tk.Tk()
root.title("Test app")
root.geometry("600x400")

button = tk.Button(root, text="Click Here", command=on_click)
button.pack()

root.mainloop()