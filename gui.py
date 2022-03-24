import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import pandas as pd
from PIL import ImageTk, Image
from threading import *

from detector import Detector
from settings import Settings

def select_file():
    filetypes = (
        ('Video Files', '.mp4 .wmv .mov'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )

def update():
    while True:
        nextFrame = Image.fromarray(det.getNextFrame())
        if nextFrame == None:
            break
        img = ImageTk.PhotoImage(nextFrame)
        label.configure(image=img)
        label.image = img

def threading():
    # Call work function
    t1 = Thread(target=update)
    t1.start()

def open_settings():
    settings = Settings()
    print(settings.result)

window = tk.Tk()
det = Detector()

window.title("MILK Detector")
window.resizable(width=False, height=False)  

# Get structure with all products available
products_file = "milk-products.csv"
products = []

try:
    data = pd.read_csv(products_file)
    for index, row in data.iterrows():
        products.append([row["NAME"], float(row["PRICE"].replace(',','.')), 0])
except:
    print(f"Products file {products_file} not found")

img_frame = tk.Frame(master=window)
ctrl_frame = tk.Frame(master=window)

text_box = tk.Text(ctrl_frame, width=32, height=28, font=("Helvetica", 8))
btn_settings = tk.Button(ctrl_frame, text="Settings...", command=open_settings)
btn_load = tk.Button(ctrl_frame, text="Load Video", command=select_file)
btn_backwards = tk.Button(ctrl_frame, text="<<", width=5)
btn_play = tk.Button(ctrl_frame, text=">", width=5, command=threading)
btn_pause = tk.Button(ctrl_frame, text="||", width=5)
btn_forward = tk.Button(ctrl_frame, text=">>", width=5)

btn_settings.grid(row=0, column=1, pady=(0,3), sticky='we', columnspan=4)
btn_load.grid(row=1, column=1, pady=(3,3), sticky='we', columnspan=4)
btn_backwards.grid(row=2, column=1, pady=(6,6))
btn_play.grid(row=2, column=2)
btn_pause.grid(row=2, column=3)
btn_forward.grid(row=2, column=4)
text_box.grid(row=3, column=1, pady=(3,0), columnspan=4)

placeholder = Image.open("data/images/cond/cond_a0237575-a2dd-11ec-a523-7085c2c6b3ed.jpg")
placeholder = placeholder.resize((870, 500), Image.ANTIALIAS)
img = ImageTk.PhotoImage(placeholder)
label = tk.Label(img_frame, image=img)
label.grid(row=0, column=0)

img_frame.grid(row=0, column=0, padx=(8,3), pady=8, rowspan=2)
ctrl_frame.grid(row=0, column=1, padx=(3,8), sticky='s')


text = f"Price List:\n\n"
for product in products:
    price = str(product[1]).split('.')
    text += f"{product[0]} - R${price[0] + ',' + price[1].ljust(2, '0')}\n"

text += f"\nShopping List:\n\n"

text_box.insert("end",text)
#text_box.delete(1.0, "end")

window.mainloop()
