import tkinter as tk
from tkinter import DoubleVar, IntVar, filedialog as fd
from tkinter.messagebox import showinfo

backdrop_color = '#CACACA'
background_color = '#D4D4D4'
border_color = "#C0C0C0"

def set_text(entry, text):
    entry.config(state='normal')

    entry.delete(0, tk.END)
    entry.insert(0, text)
    #entry.focus()
    #position = entry.index(tk.INSERT)
    #entry.icursor(position)

    entry.config(state='disabled')

def select_file(entry, selected_file):

    if selected_file == 'cfg':
        filetype = ('.cfg File', '.cfg')
    elif selected_file == 'weights':
        filetype = ('.weights File', '.weights')
    elif selected_file == 'names':
        filetype = ('.names File', '.names')
    elif selected_file == 'csv':
        filetype = ('products .csv file', '.csv')
    else:
        filetype = ('All files', '*.*')

    filename = fd.askopenfilename(
        title='Open a file',
        filetypes=[filetype])

    set_text(entry, filename)
    #showinfo(title='Selected File', message=filename)


class Settings:
    def __init__(self):

        # WINDOW CONFIGS ==================================
        # =================================================
        self.top = tk.Toplevel()
        self.top.title("Settings")
        self.top.configure(background=background_color)
        self.top.resizable(width=False, height=False) 

        # VARIABLES =======================================
        # =================================================
        self.result = None
        self.choice1 = "OK"
        self.choice2 = "DEFAULT"
        self.choice3 = "CANCEL"
        self.sliderv1 = DoubleVar(value=0.3)
        self.sliderv2 = DoubleVar(value=0.5)
        self.sliderv3 = DoubleVar(value=5/8)
        self.sliderv4 = IntVar(value=40)
        self.checkv1 = IntVar(value=0)
        self.checkv2 = IntVar(value=1)
        self.checkv3 = IntVar(value=1)
        self.checkv4 = IntVar(value=1)
        self.checkv5 = IntVar(value=1)
        self.checkv6 = IntVar(value=0)

        # MODEL SETTINGS ==================================
        # =================================================
        self.model_label = tk.Label(self.top, text="Model settings", background=background_color)
        self.model_label.grid(row=0, column=0, pady=(10,5), padx=10, sticky = 'w')
        self.model_settings = tk.Frame( master=self.top,
                                        background=backdrop_color,
                                        highlightbackground=border_color,
                                        highlightthickness=1)
        self.model_settings.grid(row=1, column=0, columnspan=5, sticky='we', padx=10)



        self.label = tk.Label(self.model_settings, text=".cfg file", background=backdrop_color)
        self.label.grid (row=0, column=0, pady=0, padx=5, sticky = 'e')
        self.entry1 = tk.Entry(self.model_settings, text=".cfg file", width=50, state='disabled')
        self.entry1.grid (row=0, column=1, pady=(5,0), padx=0, sticky='we')
        self.button = tk.Button(self.model_settings, text="Browse", width=10, command= lambda: select_file(self.entry1, 'cfg'))
        self.button.grid(row=0, column=2, pady=(5,0), padx=(10,5))

        self.label = tk.Label(self.model_settings, text=".weights file", background=backdrop_color)
        self.label.grid(row=1, column=0, pady=0, padx=5, sticky = 'e')
        self.entry2 = tk.Entry(self.model_settings, text=".weights file", state='disabled')
        self.entry2.grid(row=1, column=1, pady=(5,0), padx=0, sticky='we')
        self.button = tk.Button(self.model_settings, text="Browse", command= lambda: select_file(self.entry2, 'weights'))
        self.button.grid(row=1, column=2, pady=(5,0), padx=(10,5), sticky='we')

        self.label = tk.Label(self.model_settings, text=".names file", background=backdrop_color)
        self.label.grid(row=2, column=0, pady=0, padx=5, sticky = 'e')
        self.entry3 = tk.Entry(self.model_settings, text=".names file", state='disabled')
        self.entry3.grid(row=2, column=1, pady=(5,0), padx=0, sticky='we')
        self.button = tk.Button(self.model_settings, text="Browse", command= lambda: select_file(self.entry3, 'names'))
        self.button.grid(row=2, column=2, pady=(5,0), padx=(10,5), sticky='we')

        self.label = tk.Label(self.model_settings, text="products .csv file", background=backdrop_color)
        self.label.grid(row=3, column=0, pady=0, padx=5, sticky = 'e')
        self.entry4 = tk.Entry(self.model_settings, text="products .csv file", state='disabled')
        self.entry4.grid(row=3, column=1, pady=(5,0), padx=0, sticky='we')
        self.button = tk.Button(self.model_settings, text="Browse", command= lambda: select_file(self.entry4, 'csv'))
        self.button.grid(row=3, column=2, pady=(5,0), padx=(10,5), sticky='we')



        self.label = tk.Label(self.model_settings, text="Confidence Threshold", background=backdrop_color)
        self.label.grid(row=4, column=0, pady=5, padx=5, sticky = 'e')
        self.slider = tk.Scale(self.model_settings, 
                                from_=0.0, to=1.0, 
                                digits=3, 
                                resolution=0.05, 
                                orient='horizontal', 
                                background=backdrop_color, 
                                highlightthickness=0,
                                variable=self.sliderv1)
        self.slider.grid(row=4, column=1, pady=5, padx=(0,5), sticky='we', columnspan=2)

        self.label = tk.Label(self.model_settings, text="Non-maximum\nsuppression Threshold", background=backdrop_color)
        self.label.grid(row=5, column=0, pady=5, padx=5, sticky = 'e')
        self.slider = tk.Scale(self.model_settings, 
                                from_=0.0, to=1.0, 
                                digits=3, 
                                resolution=0.05, 
                                orient='horizontal', 
                                background=backdrop_color, 
                                highlightthickness=0,
                                variable=self.sliderv2)
        self.slider.grid(row=5, column=1, pady=5, padx=(0,5), sticky='we', columnspan=2)



        # TRACKER SETTINGS ==================================
        # =================================================
        self.tracker_label = tk.Label(self.top, text="Tracker settings", background=background_color)
        self.tracker_label.grid(row=2, column=0, pady=5, padx=10, sticky = 'w')
        self.tracker_settings = tk.Frame(master=self.top,
                                         background=backdrop_color,
                                         highlightbackground=border_color,
                                         highlightthickness=1)
        self.tracker_settings.grid(row=3, column=0, columnspan=2, padx=(10,5))

        self.slider = tk.Scale(self.tracker_settings, 
                                from_=0.0, to=1.0, 
                                digits=3,
                                resolution=0.05, 
                                orient='horizontal', 
                                background=backdrop_color, 
                                highlightthickness=0,
                                length=250,
                                label="Checking proportion",
                                variable=self.sliderv3)
        self.slider.grid(row=0, column=0, padx=10, pady=10)

        self.slider = tk.Scale(self.tracker_settings, 
                                from_=0, to=80, 
                                orient='horizontal', 
                                background=backdrop_color,
                                highlightthickness=0,
                                length=250,
                                label="Same object radius",
                                variable=self.sliderv4)
        self.slider.grid(row=1, column=0, padx=10, pady=(0,20))

        
        # DISPLAY SETTINGS ==================================
        # =================================================
        self.display_label = tk.Label(self.top, text="Display settings", background=background_color)
        self.display_label.grid(row=2, column=2, sticky = 'w')
        self.display_settings = tk.Frame(master=self.top,
                                         background=backdrop_color,
                                         highlightbackground=border_color,
                                         highlightthickness=1)
        self.display_settings.grid(row=3, column=2, columnspan=3, sticky='nswe', padx=(5,15))

        self.check = tk.Checkbutton(self.display_settings, 
                                    text='Debug detected objects',
                                    background=backdrop_color,
                                    command=self.test,
                                    variable=self.checkv1)
        self.check.grid(row=0, column=0, pady=(0,5), sticky='w')
        self.check = tk.Checkbutton(self.display_settings, 
                                    text='Display name and score',
                                    background=backdrop_color,
                                    command=self.test,
                                    variable=self.checkv2)
        self.check.grid(row=1, column=0, pady=(0,5), sticky='w')
        self.check = tk.Checkbutton(self.display_settings, 
                                    text='Display bounding boxes',
                                    background=backdrop_color,
                                    command=self.test,
                                    variable=self.checkv3)
        self.check.grid(row=2, column=0, pady=(0,5), sticky='w')
        self.check = tk.Checkbutton(self.display_settings, 
                                    text='Display tracking info (radius and id)',
                                    background=backdrop_color,
                                    command=self.test,
                                    variable=self.checkv4)
        self.check.grid(row=3, column=0, pady=(0,5), sticky='w')
        self.check = tk.Checkbutton(self.display_settings, 
                                    text='Display FPS',
                                    background=backdrop_color,
                                    command=self.test,
                                    variable=self.checkv5)
        self.check.grid(row=4, column=0, pady=(0,5), sticky='w')
        # =================================================

        self.check = tk.Checkbutton(self.top, 
                                    text='Save settings as default',
                                    background=background_color,
                                    command=self.test,
                                    variable=self.checkv6)
        self.check.grid(row=6, column=0, pady=(5,0), padx=5, sticky='w', columnspan=2)

        self.ok_btn = tk.Button(self.top, text="OK", command=self.on_press_OK)
        self.ok_btn.grid(row=7, column=0, sticky='we', pady=(5,10), padx=(10, 35))

        self.default_btn = tk.Button(self.top, text="Defaults", command=self.set_DEFAULTS)
        self.default_btn.grid(row=7, column=1, sticky='we', pady=(5,10), padx=(15, 5))

        self.cancel_btn = tk.Button(self.top, text="Cancel", command=self.on_press_CANCEL)
        self.cancel_btn.grid(row=7, column=4, sticky='we', pady=(5,10), padx=(0,10))

        self.set_DEFAULTS()
        # don't return to main part untill you close
        self.top.wait_window()

    def on_press_OK(self):
        self.result =  [
                        self.entry1.get(),
                        self.entry2.get(),
                        self.entry3.get(),
                        self.entry4.get(),
                        self.sliderv1.get(),
                        self.sliderv2.get(),
                        self.sliderv3.get(),
                        self.sliderv4.get(),
                        self.checkv1.get(),
                        self.checkv2.get(),
                        self.checkv3.get(),
                        self.checkv4.get(),
                        self.checkv5.get()]

        self.top.destroy()

    def on_press_CANCEL(self):
        self.result = self.choice3
        self.top.destroy()

    def set_DEFAULTS(self):

        lines = []
        with open('defaults/configs.txt') as f:
            lines = f.readlines()


        set_text(self.entry1, lines[0].split('=')[1].rstrip())
        set_text(self.entry2, lines[1].split('=')[1].rstrip())
        set_text(self.entry3, lines[2].split('=')[1].rstrip())
        set_text(self.entry4, lines[3].split('=')[1].rstrip())

        self.sliderv1.set(float(lines[4].split('=')[1].rstrip()))
        self.sliderv2.set(float(lines[5].split('=')[1].rstrip()))
        self.sliderv3.set(float(lines[6].split('=')[1].rstrip()))
        self.sliderv4.set(int(lines[7].split('=')[1].rstrip()))
        self.checkv1.set(int(lines[8].split('=')[1].rstrip()))
        self.checkv2.set(int(lines[9].split('=')[1].rstrip()))
        self.checkv3.set(int(lines[10].split('=')[1].rstrip()))
        self.checkv4.set(int(lines[11].split('=')[1].rstrip()))
        self.checkv5.set(int(lines[12].split('=')[1].rstrip()))


    def test(self):
        print('test')

def open_settings():
    settings = Settings()
    print(settings.result)

open_settings()