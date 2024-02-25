import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from keras.models import load_model

# Load model
model = load_model("child_detection.h5")

# Initialize GUI
top = tk.Tk()
top.geometry("800x600")
top.title("Child or Not Detector")
top.configure(background="#cdcdcd")

# Intialize labels (for age and sex)
label1 = Label(top, background="#cdcdcd", font=("arial", 15, "bold"))
label2 = Label(top, background="#cdcdcd", font=("arial", 15, "bold"))
sign_image = Label(top)


# Custom functions for 1) prediction using model, 2) showing detect button, 3) upload image
def detect(file_path):
    global label_packed
    image = Image.open(file_path)
    image = image.resize((48, 48))
    image = np.expand_dims(image, axis=0)
    image = np.array(image)
    image = np.delete(image, 0, 1)
    image = np.resize(image, (64, 64, 3))
    print(image.shape)
    child_or_not = ["Yes", "No"]
    image = np.array([image]) / 255
    pred = model.predict(image)
    age = int(np.round(pred[1][0]))
    child = int(np.round(pred[0][0]))
    # print("Predicted Age is", str(age))
    print("Predicted Child or Not is", child_or_not[child])
    # label1.configure(foreground="#011638", text="Predicted Child (Yes/No)")
    label2.configure(foreground="#011638", text=child_or_not[child])
    return


def show_detect_button(file_path):
    detect_b = Button(
        top, text="Detect Image", command=lambda: detect(file_path), padx=10, pady=5
    )
    detect_b.configure(
        background="#364156", foreground="#ffffff", font=("arial", 10, "bold")
    )
    detect_b.place(relx=0.79, rely=0.46)
    return


def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(uploaded)

        sign_image.configure(image=im)
        sign_image.image = im
        # label1.configure(text="")
        label2.configure(text="")
        show_detect_button(file_path)
    except:
        pass


upload = Button(top, text="Upload an Image", command=upload_image, padx=10, pady=5)
upload.configure(background="#364156", foreground="#ffffff", font=("arial", 10, "bold"))
upload.pack(side="bottom", pady=50)
sign_image.pack(side="bottom", expand=True)
# label1.pack(side="bottom", expand=True)
label2.pack(side="bottom", expand=True)
heading = Label(top, text="Child or Not Detector", pady=20, font=("arial", 20, "bold"))
heading.configure(background="#cdcdcd", foreground="#364156")
heading.pack()
top.mainloop()
