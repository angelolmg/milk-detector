import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, showerror, showwarning
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
        if video_playing:
            imgMatrix = det.getNextFrame()

            if isinstance(imgMatrix, type(None)):
                global feeds
                feeds = []
                print('Video ended.')
                return

            nextFrame = Image.fromarray(imgMatrix)
            img = ImageTk.PhotoImage(nextFrame)
            label.configure(image=img)
            label.image = img
        else:
            continue

def threading():
    # Call work function
    global feeds, video_feed
    video_feed = Thread(target=update)
    video_feed.start()
    feeds.append(video_feed)

def open_settings():
    global configuration
    settings = Settings(configuration, get_defaults())

    if settings.result: 
        configuration = settings.result
    #else: showwarning(title='Configuration Warning', message="No new configuration applied.")

    apply_settings(configuration)

def apply_settings(new_config=None):
    global det
    det = Detector(video_path, new_config)

def get_defaults():
        try:
            lines = []
            with open('defaults/configuration.txt') as f:
                lines = f.readlines()
            print('Getting defaults from file.')
        except:
            showerror(title='Configuration Error', message="The file 'defaults/configuration.txt' is missing.")
            return None

        configs =  [lines[0].split('=')[1].rstrip(),
                    lines[1].split('=')[1].rstrip(),
                    lines[2].split('=')[1].rstrip(),
                    lines[3].split('=')[1].rstrip(),
                    float(lines[4].split('=')[1].rstrip()),
                    float(lines[5].split('=')[1].rstrip()),
                    float(lines[6].split('=')[1].rstrip()),
                    int(lines[7].split('=')[1].rstrip()),
                    bool(int(lines[8].split('=')[1].rstrip())),
                    bool(int(lines[9].split('=')[1].rstrip())),
                    bool(int(lines[10].split('=')[1].rstrip())),
                    bool(int(lines[11].split('=')[1].rstrip())),
                    bool(int(lines[12].split('=')[1].rstrip()))
                    ]

        return configs

def play_video():
    if len(feeds) > 0:
        global video_playing
        video_playing = True
        print('video resume.')

    else:
        print('video init.')
        threading()


def pause_video():
    global video_playing
    video_playing = False
    
window = tk.Tk()
video_path = "data2/videos/milk_cond7.mp4"
configuration = get_defaults()
det = Detector(video_path, configuration)

video_feed = None
video_playing = True
feeds = []

window.title("MILK Detector")
window.resizable(width=False, height=False)  

# Get structure with all products available
products = []
if det is not None:
    products = det.get_products()

img_frame = tk.Frame(master=window)
ctrl_frame = tk.Frame(master=window)

text_box = tk.Text(ctrl_frame, width=32, height=28, font=("Helvetica", 8))
btn_settings = tk.Button(ctrl_frame, text="Settings...", command=open_settings)
btn_load = tk.Button(ctrl_frame, text="Load Video", command=select_file)
btn_backwards = tk.Button(ctrl_frame, text="<<", width=5)
btn_play = tk.Button(ctrl_frame, text=">", width=5, command=play_video)
btn_pause = tk.Button(ctrl_frame, text="||", width=5, command=pause_video)
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
