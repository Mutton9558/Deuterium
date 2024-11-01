import yt_dlp
import re
import os
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import time
import threading

def on_entry_click(event):
   if ans.get() == "e.g. (https://www.youtube.com/watch?v=dQw4w9WgXcQ)":
      ans.delete(0, END)
      ans.configure(foreground="black")

def on_focus_out(event):
   if ans.get() == "":
      ans.insert(0, "e.g. (https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
      ans.configure(foreground="gray")

def sanitize(filename):
   return re.sub(r'[<>:"/\\|?*]', '_', filename)[:255]

def update_progress(progress_value, status_text):
   progress_bar['value'] = progress_value
   status_label.config(text=status_text)

def download_video():
   link = ans.get().strip()
   if not link:
      messagebox.showwarning("Input Error", "Please enter a valid YouTube link.")
      return

   download_dir = filedialog.askdirectory(title="Select Download Location")
   if not download_dir:
      messagebox.showwarning("Directory Selection", "Please select a valid directory.")
      return

   progress_bar['value'] = 0
   status_label.config(text="Starting download...")

   def run_download():
      last_progress = -1  # Track the last progress to throttle updates

      def progress_hook(d):
         nonlocal last_progress  # Access the outer scope variable
         if d['status'] == 'downloading':
               downloaded = d.get('_percent_str', '0.0%')
               pattern = r"\b\d+\.\d+\b"
               match = re.search(pattern, downloaded)
               if match:
                  current_progress = float(match.group())
                  if int(current_progress) % 5 == 0 and current_progress != last_progress:  # Update every 5%
                     last_progress = int(current_progress)
                     root.after(0, update_progress, current_progress, f"Downloading: {downloaded}")
         elif d['status'] == 'finished':
               root.after(0, update_progress, 100, "Download complete. Finalizing...")

      try:
         ydl_opts = {
               'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
               'noplaylist': True,
               'progress_hooks': [progress_hook],
               'postprocessors': [{
                  'key': 'FFmpegVideoConvertor',
                  'preferedformat': 'mp4',
               }],
               'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
               'quiet': True,
         }

         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
               info_dict = ydl.extract_info(link, download=True)
               filename = ydl.prepare_filename(info_dict)
               video_title = info_dict.get('title', 'video')
               sanitized_filename = os.path.join(download_dir, sanitize(video_title + '.mp4'))
               os.rename(filename, sanitized_filename)

         current_time = time.time()
         os.utime(sanitized_filename, (current_time, current_time))

         messagebox.showinfo("Download Complete", f"Video downloaded as: {sanitized_filename}")
         root.after(0, update_progress, 100, "Download complete.")

      except Exception as e:
         messagebox.showerror("Download Error", f"An error occurred: {str(e)}")
         root.after(0, update_progress, 0, "An error occurred.")

   # Start the download in a new thread
   threading.Thread(target=run_download, daemon=True).start()

root = Tk()
root.title('Deuterium')

image_path = "Deuterium App\\deuterium_bg.png"
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

submitBtn = Button(root, text="Submit", command=download_video)
submitBtn.pack(pady=(5,0), ipadx=5)

progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode='determinate')
progress_bar.pack(pady=10)

status_label = Label(root, text="", font=('Helvetica', 10), bg="#23242a", fg="white")
status_label.pack(pady=5)

image_label = Label(root, image=img, bg="#23242a")
image_label.pack(anchor="w")

root.minsize(854, 480)
root.configure(bg="#23242a")
root.mainloop()
