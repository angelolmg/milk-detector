import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, showerror, showwarning
from PIL import ImageTk, Image
from threading import *
import time

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
    '''
    showinfo(
        title='Selected File',
        message=filename
    )
    '''
    load_video(filename)

def update(): 
    while True:
        if video_playing:
            imgMatrix = det.getNextFrame()

            if isinstance(imgMatrix, type(None)):
                end_video()
                return

            nextFrame = Image.fromarray(imgMatrix)
            img = ImageTk.PhotoImage(nextFrame)
            label.configure(image=img)
            label.image = img
        else:
            if len(feeds) == 0:
                print('gui.py - No feeds available. Returning this thread.')
                return
            continue

def threading():
    # Call work function
    global feeds, video_feed
    print('gui.py - Creating a new video thread.')
    video_feed = Thread(target=update)
    video_feed.start()
    feeds.append(video_feed)

def open_settings():
    global configuration
    settings = Settings(configuration, fallback_config)

    if settings.result:
        print('gui.py - New configurations received.')
        configuration = settings.result
    #else: showwarning(title='Configuration Warning', message="No new configuration applied.")

    if video_path != "":
        print('gui.py - Loading video again with new configurations.')
        load_video(video_path)

    else:
        print("gui.py - Can't load video again because there's no video path.")

def apply_settings(video_path="", new_config=None):
    global det
    det = Detector(video_path, new_config)


def get_default_configuration():
        try:
            lines = []
            with open('defaults/configuration.txt') as f:
                lines = f.readlines()
            print('gui.py - Getting defaults from file.')
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
    global video_playing, det

    if len(feeds) > 0:      # Feed available (for pause/unpause)
        video_playing = True
        print('gui.py - Video resume.')

    elif det is not None:   # Video ended, old detector
        video_playing = True

        if det.video_over:
            det = Detector(video_path, configuration)
            print('gui.py - Video reloaded.')
            fill_shoppinglist()

        threading()
        print('gui.py - Video initiated.')

    else:                   # No feed available & detector offline
        video_playing = False
        showerror(title='Video path Error', message="No video path provided. Please load a video first.")

def load_video(path):
    global det, video_path
    video_path = path
    det = Detector(video_path, configuration)
    print('gui.py - Video loaded.')

    fill_shoppinglist()
    play_video()

def pause_video():
    global video_playing
    video_playing = False
    print('gui.py - Video paused.')

def end_video():    # Pauses then clears the feed list
    pause_video()

    global feeds
    feeds = []
    print('gui.py - Video ended.')

def fill_shoppinglist():
    global product, text_box

    # Get structure with all products available
    products = []
    if det is not None:
        products = det.get_products()
        print('gui.py - Filling shopping list.')

    text_box.delete(1.0, "end")

    text = f"Price List:\n\n"
    for product in products:
        price = str(product[1]).split('.')
        text += f"{product[0]} - R${price[0] + ',' + price[1].ljust(2, '0')}\n"

    text += f"\nShopping List:\n\n"

    text_box.insert("end",text)
    
    

window = tk.Tk()
#video_path = "data2/videos/milk_cond7.mp4"
video_path = ""
configuration = get_default_configuration()
fallback_config = configuration.copy()
#det = Detector(video_path, configuration)

det = None
video_feed = None
video_playing = False
feeds = []

window.title("MILK Detector")
window.resizable(width=False, height=False)  

img_frame = tk.Frame(master=window)
ctrl_frame = tk.Frame(master=window)

text_box = tk.Text(ctrl_frame, width=32, height=28, font=("Helvetica", 8))
btn_settings = tk.Button(ctrl_frame, text="Settings...", command=open_settings)
btn_load = tk.Button(ctrl_frame, text="Load Video", command=select_file)
#btn_backwards = tk.Button(ctrl_frame, text="<<", width=5)
btn_play = tk.Button(ctrl_frame, text=">", width=5, command=play_video)
btn_pause = tk.Button(ctrl_frame, text="||", width=5, command=pause_video)
btn_forward = tk.Button(ctrl_frame, text=">>", width=5)

btn_settings.grid(row=0, column=1, pady=(0,3), sticky='we', columnspan=4)
btn_load.grid(row=1, column=1, pady=(3,3), sticky='we', columnspan=4)
#btn_backwards.grid(row=2, column=1, pady=(6,6))
btn_play.grid(row=2, column=1, padx=(12,0), pady=(6,6))
btn_pause.grid(row=2, column=2)
btn_forward.grid(row=2, column=3)
text_box.grid(row=3, column=1, pady=(3,0), columnspan=4)

placeholder = Image.open("data/images/cond/cond_a0237575-a2dd-11ec-a523-7085c2c6b3ed.jpg")
placeholder = placeholder.resize((870, 500), Image.ANTIALIAS)
img = ImageTk.PhotoImage(placeholder)
label = tk.Label(img_frame, image=img)
label.grid(row=0, column=0)

img_frame.grid(row=0, column=0, padx=(8,3), pady=8, rowspan=2)
ctrl_frame.grid(row=0, column=1, padx=(3,8), sticky='s')

fill_shoppinglist()

window.mainloop()
