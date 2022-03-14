import tkinter as tk
import pandas as pd
from PIL import ImageTk, Image

window = tk.Tk()

window.title("MILK Detector")
window.resizable(width=False, height=False)
#window.geometry("1100x500")

#window.columnconfigure(0, weight=1) 
#window.rowconfigure(3, weight=1)      

# Get structure with all products available
products_file = "milk-products1.csv"
products = []

try:
    data = pd.read_csv(products_file)
    for index, row in data.iterrows():
        products.append([row["NAME"], float(row["PRICE"].replace(',','.')), 0])
except:
    print(f"Products file {products_file} not found")


img_frame = tk.Frame(master=window)
ctrl_frame = tk.Frame(master=window)

placeholder = Image.open("data/images/cond/cond_a0237575-a2dd-11ec-a523-7085c2c6b3ed.jpg")
placeholder = placeholder.resize((870, 500), Image.ANTIALIAS)
img = ImageTk.PhotoImage(placeholder)
label = tk.Label(img_frame, image=img)

text_box = tk.Text(ctrl_frame, width=32, height=28, font=("Helvetica", 8))
btn_settings = tk.Button(ctrl_frame, text="Settings...")
btn_load = tk.Button(ctrl_frame, text="Load Video")
btn_backwards = tk.Button(ctrl_frame, text="<<", width=5)
btn_play = tk.Button(ctrl_frame, text=">", width=5)
btn_forward = tk.Button(ctrl_frame, text=">>", width=5)

btn_settings.grid(row=0, column=1, pady=(0,3), sticky='we', columnspan=3)
btn_load.grid(row=1, column=1, pady=(3,3), sticky='we', columnspan=3)
btn_backwards.grid(row=2, column=1, pady=(6,6))
btn_play.grid(row=2, column=2)
btn_forward.grid(row=2, column=3)
text_box.grid(row=3, column=1, pady=(3,0), columnspan=3)

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