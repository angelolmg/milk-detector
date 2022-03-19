import tkinter as tk

backdrop_color = '#CACACA'
background_color = '#D4D4D4'
border_color = "#C0C0C0"

class Settings:
    def __init__(self):

        self.top = tk.Toplevel()
        self.top.title("Settings")
        self.top.configure(background=background_color)
        self.top.resizable(width=False, height=False) 

        self.result = None

        self.choice1 = "OK"
        self.choice2 = "DEFAULT"
        self.choice3 = "CANCEL"

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
        self.entry = tk.Entry(self.model_settings, text=".cfg file", state='disabled', width=50)
        self.entry.grid (row=0, column=1, pady=(5,0), padx=0, sticky='we')
        self.button = tk.Button(self.model_settings, text="Browse", command=self.test, width=10)
        self.button.grid(row=0, column=2, pady=(5,0), padx=(10,5))

        self.label = tk.Label(self.model_settings, text=".weights file", background=backdrop_color)
        self.label.grid(row=1, column=0, pady=0, padx=5, sticky = 'e')
        self.entry = tk.Entry(self.model_settings, text=".weights file", state='disabled')
        self.entry.grid(row=1, column=1, pady=(5,0), padx=0, sticky='we')
        self.button = tk.Button(self.model_settings, text="Browse", command=self.test)
        self.button.grid(row=1, column=2, pady=(5,0), padx=(10,5), sticky='we')

        self.label = tk.Label(self.model_settings, text=".names file", background=backdrop_color)
        self.label.grid(row=2, column=0, pady=0, padx=5, sticky = 'e')
        self.entry = tk.Entry(self.model_settings, text=".names file", state='disabled')
        self.entry.grid(row=2, column=1, pady=(5,0), padx=0, sticky='we')
        self.button = tk.Button(self.model_settings, text="Browse", command=self.test)
        self.button.grid(row=2, column=2, pady=(5,0), padx=(10,5), sticky='we')

        self.label = tk.Label(self.model_settings, text="products .csv file", background=backdrop_color)
        self.label.grid(row=3, column=0, pady=0, padx=5, sticky = 'e')
        self.entry = tk.Entry(self.model_settings, text="products .csv file", state='disabled')
        self.entry.grid(row=3, column=1, pady=(5,0), padx=0, sticky='we')
        self.button = tk.Button(self.model_settings, text="Browse", command=self.test)
        self.button.grid(row=3, column=2, pady=(5,0), padx=(10,5), sticky='we')



        self.label = tk.Label(self.model_settings, text="Confidence Threshold", background=backdrop_color)
        self.label.grid(row=4, column=0, pady=5, padx=5, sticky = 'e')
        self.slider = tk.Scale(self.model_settings, 
                                from_=0.0, to=1.0, 
                                digits=3, 
                                resolution=0.05, 
                                orient='horizontal', 
                                background=backdrop_color, 
                                highlightthickness=0)
        self.slider.grid(row=4, column=1, pady=5, padx=(0,5), sticky='we', columnspan=2)

        self.label = tk.Label(self.model_settings, text="Non-maximum\nsuppression Threshold", background=backdrop_color)
        self.label.grid(row=5, column=0, pady=5, padx=5, sticky = 'e')
        self.slider = tk.Scale(self.model_settings, 
                                from_=0.0, to=1.0, 
                                digits=3, 
                                resolution=0.05, 
                                orient='horizontal', 
                                background=backdrop_color, 
                                highlightthickness=0)
        self.slider.grid(row=5, column=1, pady=5, padx=(0,5), sticky='we', columnspan=2)


        # =================================================


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
                                label="Checking proportion")
        self.slider.grid(row=0, column=0, padx=10, pady=(5,10))

        self.slider = tk.Scale(self.tracker_settings, 
                                from_=10, to=100, 
                                orient='horizontal', 
                                background=backdrop_color,
                                highlightthickness=0,
                                length=250,
                                label="Same object radius")
        self.slider.grid(row=1, column=0, padx=10, pady=(0,10))

        # =================================================
        
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
                                    text='Debug objects',
                                    background=backdrop_color,
                                    command=self.test)
        self.check.grid(row=0, column=0, pady=(0,5), sticky='w')
        self.check = tk.Checkbutton(self.display_settings, 
                                    text='Display FPS',
                                    background=backdrop_color,
                                    command=self.test)
        self.check.grid(row=1, column=0, pady=(0,5), sticky='w')
        self.check = tk.Checkbutton(self.display_settings, 
                                    text='Display total price',
                                    background=backdrop_color,
                                    command=self.test)
        self.check.grid(row=2, column=0, pady=(0,5), sticky='w')
        # =================================================


        self.ok_btn = tk.Button(self.top, text="OK", command=self.on_press_OK)
        self.ok_btn.grid(row=6, column=0, sticky='we', pady=10, padx=(10, 35))

        self.default_btn = tk.Button(self.top, text="Defaults", command=self.on_press_DEFAULTS)
        self.default_btn.grid(row=6, column=1, sticky='we', pady=0, padx=(15, 5))

        self.cancel_btn = tk.Button(self.top, text="Cancel", command=self.on_press_CANCEL)
        self.cancel_btn.grid(row=6, column=4, sticky='we', pady=0, padx=(0,10))

        # don't return to main part untill you close
        self.top.wait_window()

    def on_press_OK(self):
        self.result = self.choice1
        self.top.destroy()

    def on_press_DEFAULTS(self):
        self.result = self.choice2
        self.top.destroy()

    def on_press_CANCEL(self):
        self.result = self.choice3
        self.top.destroy()

    def test(self):
        print('test')

    

def open_settings():
    settings = Settings()
    print(settings.result)

#open_settings()

