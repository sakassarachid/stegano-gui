import threading
import time
import numpy as np
from customtkinter import *
from tkinterdnd2 import TkinterDnD
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror
from tkinter import Canvas, PhotoImage
from stegano import lsb
from PIL import Image, ImageTk
from lsb import embed_secret_message
from dct import dct_disguise
from pdv import apply_diff
from dhwt import embed_dhwt

# Set custom colors and fonts
set_appearance_mode("light")

custom_font = ("Arial", 12)
title_font = ("Helvetica", 18, "bold")
button_font = ("Helvetica", 14, "bold")

# Custom button colors
button_bg_color = "#450037"  # violet color
button_fg_color = "white"    # White color

# Create a custom Tkinter class that supports drag-and-drop
class Tk(CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

# Function to show an error message
def show_error():
    showerror("ERROR", "Expected a PNG image ")

# Initialize global variables
FILE = None
progressbar = None
img = None
frame = None

# Function to encode text in an image
def encode_in_image(text):
    global progressbar, img

    img = lsb.hide(FILE, text)
    progressbar.stop()

    for x in range(0, 101):
        progressbar.set(1 * x / 100)
        root.update()

    time.sleep(0.5)
    for widget in frame.winfo_children():
        widget.destroy()

    save_btn = CTkButton(frame, text="Save and Download the Image",fg_color="transparent", font=button_font,
                         bg_color=button_bg_color, command=save)
    save_btn.place(anchor="center", relx=0.5, rely=0.5)

    go_back = CTkButton(frame, text=" Back",fg_color="transparent", font=button_font,
                        bg_color=button_bg_color, command=home)
    go_back.place(anchor="nw", x=20, y=20)


# Function to save the encoded image
def save():
    file = asksaveasfilename()
    if file != "":
        if file.endswith(".png"):
            img.save(file)
        else:
            img.save(file + ".png")

# Function to encode text
def encode(text):
    global progressbar

    for widget in frame.winfo_children():
        widget.destroy()
    # Load the background image for the current UI
    ui_bg_img = Image.open("backgr.jpeg")  # the actual file path
    ui_bg_img = ui_bg_img.resize((800, 800), Image.ANTIALIAS)
    ui_bg_img = ImageTk.PhotoImage(ui_bg_img)

    # Create a label to display the background image
    ui_bg_label = CTkLabel(frame, text="", image=ui_bg_img)
    ui_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    description = CTkLabel(frame, text="Loading.....", font=title_font, anchor="c")
    description.pack(fill="x", pady=20, padx=40)
    progressbar = CTkProgressBar(frame, height=20, corner_radius=3)
    progressbar.pack(expand=True, fill="x", padx=20)
    progressbar.start()
    t1 = threading.Thread(target=encode_in_image, args=(text,))
    t1.start()


def encode_ui():
    for widget in frame.winfo_children():
        widget.destroy()
    # Load the background image for the current UI
    ui_bg_img = Image.open("backgr.jpeg")  #actual file path
    ui_bg_img = ui_bg_img.resize((800, 800), Image.ANTIALIAS)
    ui_bg_img = ImageTk.PhotoImage(ui_bg_img)

    # Create a label to display the background image
    ui_bg_label = CTkLabel(frame, text="", image=ui_bg_img)
    ui_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    data_label = CTkLabel(frame, text="Select an option:", font=title_font)
    data_label.pack(pady=20)

    text_button = CTkButton(frame, text="Hide Text", fg_color="transparent", font=button_font, bg_color=button_bg_color, command=encode_text_ui)
    text_button.pack(side="left", padx=20, pady=(0, 20))

    image_button = CTkButton(frame, text="Hide Image", fg_color="transparent", font=button_font, bg_color=button_bg_color, command=encode_img_ui)
    image_button.pack(side="right", padx=20, pady=(0, 20))

    go_back = CTkButton(frame, text=" Back", fg_color="transparent", font=button_font,
                        bg_color=button_bg_color, command=home)
    go_back.place(anchor="nw", x=0, y=0)

def decode_ui():
    for widget in frame.winfo_children():
        widget.destroy()
    try:
        data = lsb.reveal(FILE)
        text = CTkLabel(frame, text=data, font=title_font, wraplength=500, fg_color="transparent",
                        bg_color="transparent")
        text.place(anchor="center", relx=0.5, rely=0.5)

        go_back = CTkButton(frame, text=" Back", fg_color="transparent", font=button_font,
                            bg_color=button_bg_color, command=home)
        go_back.place(anchor="nw", x=0, y=0)
    except Exception as e:
        showerror("Error", e)
        go_back = CTkButton(frame, text=" Back", fg_color="transparent", font=button_font,
                            bg_color=button_bg_color, command=home)
        go_back.place(anchor="nw", x=0, y=0)

def encode_or_decode_ui():
    for widget in frame.winfo_children():
        widget.destroy()

    # Load the background image for the current UI
    ui_bg_img = Image.open("backgr.jpeg")  #the actual file path
    ui_bg_img = ui_bg_img.resize((800, 800), Image.ANTIALIAS)
    ui_bg_img = ImageTk.PhotoImage(ui_bg_img)

    # Create a label to display the background image
    ui_bg_label = CTkLabel(frame, text="", image=ui_bg_img)
    ui_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Add your UI elements here
    encode_btn = CTkButton(frame, fg_color="transparent", text="Hide data in an image ", font=button_font, bg_color=button_bg_color, command=encode_gui_inter)
    encode_btn.pack(expand=True, fill="both", padx=20, pady=(40, 20))

    decode_btn = CTkButton(frame, fg_color="transparent", text="Extract data from an image ", font=button_font, bg_color=button_bg_color, command=choose_file_decod)
    decode_btn.pack(expand=True, fill="both", padx=20, pady=(0, 20))


def encode_gui_inter():
    # Create the landing page frame
    for widget in frame.winfo_children():
        widget.destroy()
    # Load the background image for the current UI
    ui_bg_img = Image.open("backgr.jpeg")  #  the actual file path
    ui_bg_img = ui_bg_img.resize((800, 800), Image.ANTIALIAS)
    ui_bg_img = ImageTk.PhotoImage(ui_bg_img)

    # Create a label to display the background image
    ui_bg_label = CTkLabel(frame, text="", image=ui_bg_img)
    ui_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    frame1 = CTkFrame(frame)
    frame1.pack(padx=20, pady=20, expand=True, fill="both")

    # Create a label on the landing page
    choose_btn = CTkButton(frame1,fg_color="transparent",font=button_font,bg_color=button_bg_color, text=" Choose an image ", anchor="c",
                           command=lambda: choose_file_encod())
    choose_btn.place(anchor="center", relx=0.5, rely=0.5)

    go_back = CTkButton(frame, text="Back", fg_color="transparent", font=button_font, bg_color=button_bg_color,
                        command=home)
    go_back.place(anchor="nw", x=0, y=0)

    landing_label = CTkLabel(frame1, text="Choose an image", font=title_font)
    landing_label.pack(side="top", pady=20)
    # landing_label.bind("<Button-1>", lambda e: choose_file_encod())
    landing_label.bind("<Enter>", lambda e: frame1.configure(fg_color="#814007"))
    landing_label.bind("<Leave>", lambda e: frame1.configure(fg_color="#000000"))


def choose_file_encod():
    for widget in frame.winfo_children():
        widget.destroy()
    file = askopenfilename()
    if file != "":
        if file.endswith(".png") or file.endswith(".PNG"):
            global FILE
            FILE = file
            encode_ui()

        else:
            show_error()
    else:
        home()


def choose_file_decod():
    file = askopenfilename()

    if file != "":
        if file.endswith(".png") or file.endswith(".PNG"):
            global FILE
            FILE = file
            decode_ui()
        else:
            show_error()


def encode_text_ui():
    for widget in frame.winfo_children():
        widget.destroy()

    # Load the background image for the current UI
    ui_bg_img = Image.open("backgr.jpeg")  #the actual file path
    ui_bg_img = ui_bg_img.resize((800, 800), Image.ANTIALIAS)
    ui_bg_img = ImageTk.PhotoImage(ui_bg_img)

    # Create a label to display the background image
    ui_bg_label = CTkLabel(frame, text="", image=ui_bg_img)
    ui_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    method_btn = CTkButton(frame, fg_color="transparent", font=button_font, bg_color=button_bg_color,
                           text="Select a method ", anchor="c",
                           command=lambda: encode_txt_ui())
    method_btn.place(anchor="center", relx=0.5, rely=0.5)

    go_back = CTkButton(frame, text=" Back", fg_color="transparent", font=button_font,
                        bg_color=button_bg_color, command=encode_ui)
    go_back.place(anchor="nw", x=0, y=0)

def encode_txt_ui():
    for widget in frame.winfo_children():
        widget.destroy()

    # Load the background image for the current UI
    ui_bg_img = Image.open("backgr.jpeg")  #the actual file path
    ui_bg_img = ui_bg_img.resize((800, 800), Image.ANTIALIAS)
    ui_bg_img = ImageTk.PhotoImage(ui_bg_img)

    # Create a label to display the background image
    ui_bg_label = CTkLabel(frame, text="", image=ui_bg_img)
    ui_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    data = CTkTextbox(frame, height=100, font=custom_font)
    data.pack(expand=True, fill="both", padx=20, pady=40)

    # Use either pack or grid consistently
    dct_btn = CTkButton(frame, fg_color="transparent", font=button_font, bg_color=button_bg_color, text="DCT",
                        anchor="c", command=lambda: encode(data.get(0.0, "end")))
    dct_btn.pack(side="left", padx=20, pady=40)

    lsb_btn = CTkButton(frame, fg_color="transparent", font=button_font, bg_color=button_bg_color, text="LSB",
                        anchor="c", command=lambda: encode(data.get(0.0, "end")))
    lsb_btn.pack(side="right", padx=20, pady=40)

    diff_btn = CTkButton(frame, fg_color="transparent", font=button_font, bg_color=button_bg_color, text="PDV",
                         anchor="c", command=lambda: encode(data.get(0.0, "end")))
    diff_btn.pack(expand=True, fill="both", padx=20, pady=40)

    dhwt_btn = CTkButton(frame, fg_color="transparent", font=button_font, bg_color=button_bg_color, text="DHWT",
                         anchor="c", command=lambda: encode(data.get(0.0, "end")))
    dhwt_btn.pack(expand=True, fill="both", padx=20, pady=40)

    go_back = CTkButton(frame, text=" Back", fg_color="transparent", font=button_font,
                        bg_color=button_bg_color, command=home)
    go_back.place(anchor="nw", x=0, y=0)


def encode_img_ui():
    for widget in frame.winfo_children():
        widget.destroy()

    secret_image = askopenfilename()

    # Load the background image for the current UI
    ui_bg_img = Image.open("backgr.jpeg")  #the actual file path
    ui_bg_img = ui_bg_img.resize((800, 800), Image.ANTIALIAS)
    ui_bg_img = ImageTk.PhotoImage(ui_bg_img)

    # Create a label to display the background image
    ui_bg_label = CTkLabel(frame, text="", image=ui_bg_img)
    ui_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    if secret_image != "":
        support_image = FILE
        if support_image != "":
            encode_btn = CTkButton(frame, fg_color="transparent", font=button_font, bg_color=button_bg_color,
                                   text="Select a method ", anchor="c", command=lambda: encode_image(secret_image, support_image))
            encode_btn.place(anchor="center", relx=0.5, rely=0.5)

    go_back = CTkButton(frame, text=" Back", fg_color="transparent", font=button_font,
                        bg_color=button_bg_color, command=home)
    go_back.place(anchor="nw", x=0, y=0)


def encode_image(secret_image, support_image):
    for widget in frame.winfo_children():
        widget.destroy()

    # Load the background image for the current UI
    ui_bg_img = Image.open("backgr.jpeg")  #the actual file path
    ui_bg_img = ui_bg_img.resize((800, 800), Image.ANTIALIAS)
    ui_bg_img = ImageTk.PhotoImage(ui_bg_img)

    # Create a label to display the background image
    ui_bg_label = CTkLabel(frame, text="", image=ui_bg_img)
    ui_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    dct_btn = CTkButton(frame, fg_color="transparent", font=button_font, bg_color=button_bg_color, text="DCT", anchor="c",
                        command=lambda: dct(secret_image, support_image))
    dct_btn.grid(row=0, column=0, padx=20, pady=40, sticky="nsew")


    lsb_btn = CTkButton(frame, fg_color="transparent", font=button_font, bg_color=button_bg_color, text="LSB", anchor="c",
                        command=lambda: lsbk(support_image, secret_image))
    lsb_btn.grid(row=0, column=1, padx=20, pady=40, sticky="nsew")

    diff_btn = CTkButton(frame, fg_color="transparent", font=button_font, bg_color=button_bg_color, text="PDV", anchor="c",
                         command=lambda: diff_method(support_image, secret_image))
    diff_btn.grid(row=1, column=0, padx=20, pady=40, sticky="nsew")

    dhwt_btn = CTkButton(frame, fg_color="transparent", font=button_font, bg_color=button_bg_color, text="DHWT", anchor="c",
                         command=lambda: dhwt(support_image, secret_image))
    dhwt_btn.grid(row=1, column=1, padx=20, pady=40, sticky="nsew")

    # Adjusting row and column weights for expansion
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)

    go_back = CTkButton(frame, text=" Back", fg_color="transparent", font=button_font,
                        bg_color=button_bg_color, command=home)
    go_back.place(anchor="nw", x=0, y=0)



def dct(secret_image, support_image):
    # Perform DCT steganography
    global img
    img = Image.fromarray(dct_disguise(secret_image, support_image, alpha=0.01))


    for widget in frame.winfo_children():
        widget.destroy()
    # Load the background image for the current UI
    ui_bg_img = Image.open("backgr.jpeg")  #the actual file path
    ui_bg_img = ui_bg_img.resize((800, 800), Image.ANTIALIAS)
    ui_bg_img = ImageTk.PhotoImage(ui_bg_img)

    # Create a label to display the background image
    ui_bg_label = CTkLabel(frame, text="", image=ui_bg_img)
    ui_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    save_btn = CTkButton(frame, text="Save and Download the Image",fg_color="transparent",font=button_font,bg_color=button_bg_color, command=save)
    save_btn.place(anchor="center", relx=0.5, rely=0.5)

    go_back = CTkButton(frame, text="Back",fg_color="transparent", font=button_font,bg_color=button_bg_color, command=home)
    go_back.place(anchor="nw", x=20, y=20)


def lsbk(support_image, secret_image):
    # Perform K steganography
    global img
    img = Image.fromarray(embed_secret_message(support_image, secret_image, 1))
    for widget in frame.winfo_children():
        widget.destroy()
    # Load the background image for the current UI
    ui_bg_img = Image.open("backgr.jpeg")  #the actual file path
    ui_bg_img = ui_bg_img.resize((800, 800), Image.ANTIALIAS)
    ui_bg_img = ImageTk.PhotoImage(ui_bg_img)

    # Create a label to display the background image
    ui_bg_label = CTkLabel(frame, text="", image=ui_bg_img)
    ui_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    save_btn = CTkButton(frame, text="Save and Download the Image",fg_color="transparent", font=button_font,bg_color=button_bg_color, command=save)
    save_btn.place(anchor="center", relx=0.5, rely=0.5)

    go_back = CTkButton(frame, text="Back",fg_color="transparent", font=button_font,bg_color=button_bg_color, command=home)
    go_back.place(anchor="nw", x=20, y=20)


def diff_method(secret_image, support_image):
    global img
    img = Image.fromarray(apply_diff(support_image, secret_image))
    for widget in frame.winfo_children():
        widget.destroy()
    # Load the background image for the current UI
    ui_bg_img = Image.open("backgr.jpeg")  #the actual file path
    ui_bg_img = ui_bg_img.resize((800, 800), Image.ANTIALIAS)
    ui_bg_img = ImageTk.PhotoImage(ui_bg_img)

    # Create a label to display the background image
    ui_bg_label = CTkLabel(frame, text="", image=ui_bg_img)
    ui_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    save_btn = CTkButton(frame, text="Save and Download the Image",fg_color="transparent", font=button_font,bg_color=button_bg_color, command=save)
    save_btn.place(anchor="center", relx=0.5, rely=0.5)

    go_back = CTkButton(frame, text="Back",fg_color="transparent",font=button_font,bg_color=button_bg_color, command=home)
    go_back.place(anchor="nw", x=20, y=20)

def dhwt(support_image,secret_image):
    global img
    img = Image.fromarray(embed_dhwt(support_image, secret_image).astype(np.uint8))
    for widget in frame.winfo_children():
        widget.destroy()
    # Load the background image for the current UI
    ui_bg_img = Image.open("backgr.jpeg")  #the actual file path
    ui_bg_img = ui_bg_img.resize((800, 800), Image.ANTIALIAS)
    ui_bg_img = ImageTk.PhotoImage(ui_bg_img)

    # Create a label to display the background image
    ui_bg_label = CTkLabel(frame, text="", image=ui_bg_img)
    ui_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    save_btn = CTkButton(frame, text="Save and Download the Image",fg_color="transparent", font=button_font,bg_color=button_bg_color, command=save)
    save_btn.place(anchor="center", relx=0.5, rely=0.5)

    go_back = CTkButton(frame, text="Back",fg_color="transparent",font=button_font,bg_color=button_bg_color, command=home)
    go_back.place(anchor="nw", x=20, y=20)

def home():
    global frame
    if frame != None:
        frame.destroy()

    frame = CTkFrame(root)
    frame.pack(padx=20, pady=20, expand=True, fill="both")

    text = CTkLabel(frame, text="Stegano App", font=title_font)
    text.pack(pady=20)

    encode_or_decode_ui()


def start_app():
    # Destroy the landing page and transition to the home panel
    landing_frame.destroy()
    home()


root = Tk()
root.geometry("600x600")
root.title(" Steganography App")

# the background image
back_img = Image.open("backgr.jpeg")
back_img = back_img.resize((800, 800), Image.ANTIALIAS)
imgf = ImageTk.PhotoImage(back_img)

# the landing page to use a different background image
landing_frame = CTkFrame(root)
landing_frame.pack(padx=20, pady=20, expand=True, fill="both")

background_label = CTkLabel(landing_frame,text="", image=imgf)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

landing_label = CTkLabel(landing_frame, text="Steganography GUI", font=title_font)
landing_label.pack(pady=20)

start_button = CTkButton(landing_frame, text="Start", fg_color="transparent", font=button_font,bg_color="#450037", command=start_app)
start_button.pack(expand=True, side="bottom")

# Start the Tkinter main loop
root.mainloop()
