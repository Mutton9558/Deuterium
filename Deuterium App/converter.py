import yt_dlp
import re
from tkinter import *
from PIL import Image, ImageTk

def on_entry_click(event):
   if ans.get() == "e.g. (https://www.youtube.com/watch?v=dQw4w9WgXcQ)":
      ans.delete(0, END)
      ans.configure(foreground="black")

def on_focus_out(event):
   if ans.get() == "":
      ans.insert(0, "e.g. (https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
      ans.configure(foreground="gray")

root = Tk()
root.title('Deuterium')

image_path = "Deuterium App\deuterium_bg.png"
bottom_image = Image.open(image_path)
bottom_image = bottom_image.resize((720, 400))
img = ImageTk.PhotoImage(bottom_image)

logo = PhotoImage(file="Deuterium App\\logo.png")
root.iconphoto(True, logo)

label = Label(root, text='Welcome to Deuterium!', bg="#23242a", fg="white")
label.config(font=('Helvetica', 18, 'bold'))
label.pack(pady=(200,30))

description = Label(root, text="The Free and Reliable YouTube video to File Converter!", font=('Courier', 15), wraplength=1000, justify='center', bg="#23242a", fg="white")
description.pack(pady=(0, 30))

label2 = Label(root, text='Enter YouTube Video Link (Note: No playlists!): ', bg="#23242a", fg="white")
label2.pack()
ans = Entry(root, width=50, foreground='gray')
ans.insert(0, "e.g. (https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
ans.bind("<FocusIn>", on_entry_click)
ans.bind("<FocusOut>", on_focus_out)
ans.pack()

submitBtn = Button(root, text="Submit")
submitBtn.pack(pady=(5,0), ipadx=5)

image_label = Label(root, image=img, bg="#23242a")
image_label.pack(anchor="w")

root.minsize(854, 480)
root.configure(bg="#23242a")
root.mainloop() 


