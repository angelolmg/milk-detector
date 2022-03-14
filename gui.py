import tkinter as tk
from PIL import ImageTk, Image

window = tk.Tk()

window.title("MILK Detector")

#window.geometry("700x500")

#window.columnconfigure(0, weight=1) 
window.rowconfigure(1, weight=1)      

frame1 = tk.Frame(master=window)
frame2 = tk.Frame(master=window)
frame3 = tk.Frame(master=window)

ph = Image.open("data/images/cond/cond_a0237575-a2dd-11ec-a523-7085c2c6b3ed.jpg")
ph_w, ph_h = ph.size
ph = ph.resize((int(ph_w/2), int(ph_h/2)), Image.ANTIALIAS)
img = ImageTk.PhotoImage(ph)
label = tk.Label(frame1, image = img)


btn_settings = tk.Button(frame2, text="Settings...", width = 20)
btn_load = tk.Button(frame2, text="Load Video", width = 20)
btn_backwards = tk.Button(frame3, text="<<", width = 5)
btn_play = tk.Button(frame3, text=">", width = 5)
btn_forward = tk.Button(frame3, text=">>", width = 5)

btn_settings.grid(row=0, column=1, pady=(10,0))
btn_load.grid(row=1, column=1, pady=10)

btn_backwards.grid(row=0, column=0, padx=5)
btn_play.grid(row=0, column=1, padx=5)
btn_forward.grid(row=0, column=2, padx=5)

label.grid(row=0, column=0)
frame1.grid(row=0, column=0, sticky='nesw', rowspan=2)
frame2.grid(row=0, column=1, sticky='n')
frame3.grid(row=1, column=1, sticky='n')


window.mainloop()