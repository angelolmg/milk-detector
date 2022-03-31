import tkinter as tk
from tkinter import DoubleVar, IntVar, filedialog as fd
from tkinter.messagebox import showinfo, showerror

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
    def __init__(self, configs, fallback):

        self.fallback = fallback

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

        self.sliderv1 = DoubleVar()
        self.sliderv2 = DoubleVar()
        self.sliderv3 = DoubleVar()
        self.sliderv4 = IntVar()
        self.checkv1 = IntVar()
        self.checkv2 = IntVar()
        self.checkv3 = IntVar()
        self.checkv4 = IntVar()
        self.checkv5 = IntVar()
        self.checkv6 = IntVar()

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

        if configs is None or len(configs) is not 13:
            print('Configuration is bad. Setting fallback configutation.')
            self.set_DEFAULTS()
        else: 
            print('Configuration is good. Setting configuration.')
            self.set_configs(configs)

        # don't return to main part untill you close
        self.top.wait_window()

    def on_press_OK(self):
        self.result =  [self.entry1.get(),
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
        
        if self.checkv6.get():
            f = open("defaults/configuration.txt", "w")

            print('Rewriting defaults file.')
            f.write(   "cfg_file_path="         + self.entry1.get() + "\n\
weights_file_path="     + self.entry2.get() + "\n\
names_file_path="       + self.entry3.get() + "\n\
products_csv_file="     + self.entry4.get() + "\n\
confidence_threshold="  + str(self.sliderv1.get()) + "\n\
nms_threshold="         + str(self.sliderv2.get()) + "\n\
checking_proportion="   + str(self.sliderv3.get()) + "\n\
same_object_radius="    + str(self.sliderv4.get()) + "\n\
debug_detected_objects="+ str(self.checkv1.get()) + "\n\
display_name_score="    + str(self.checkv2.get()) + "\n\
display_bounding_boxes="+ str(self.checkv3.get()) + "\n\
display_tracking_info=" + str(self.checkv4.get()) + "\n\
display_fps="           + str(self.checkv5.get()) + "\n")
            f.close()

        self.top.destroy()

    def on_press_CANCEL(self):
        self.result = None
        self.top.destroy()

    def set_DEFAULTS(self):
        print('Setting defaults -> ' + str(self.fallback))
        self.set_configs(self.fallback)

    def set_configs(self, configs):

        try:
            set_text(self.entry1, configs[0])
            set_text(self.entry2, configs[1])
            set_text(self.entry3, configs[2])
            set_text(self.entry4, configs[3])

            self.sliderv1.set(configs[4])
            self.sliderv2.set(configs[5])
            self.sliderv3.set(configs[6])
            self.sliderv4.set(configs[7])
            self.checkv1.set(configs[8])
            self.checkv2.set(configs[9])
            self.checkv3.set(configs[10])
            self.checkv4.set(configs[11])
            self.checkv5.set(configs[12])

        except:

            if configs == self.fallback:
                showerror(title='Configuration Error', message="Fallback configuration is bad. See 'configuration.txt'.")
                return

            self.set_DEFAULTS()
            showerror(title='Configuration Error', message="Something wrong with settings. Setting defaults...")

    def test(self):
        print('test')

def open_settings():
    settings = Settings(None)
    print(settings.result)

#open_settings()