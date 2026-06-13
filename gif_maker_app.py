from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import threading

# --- Main window setup ---
root = Tk()
root.title("✨ GIF Maker 🎞️")
root.geometry("600x500")
root.config(bg="#EAF6F6")
root.resizable(False, False)

files = []
thumbnails = []

# --- Functions ---

def select_images():
    global files, thumbnails
    files = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
    )
    if not files:
        return
    
    # Clear previous thumbnails
    for widget in preview_frame.winfo_children():
        widget.destroy()

    thumbnails.clear()
    for img_path in files:
        img = Image.open(img_path)
        img.thumbnail((80, 80))
        thumb = ImageTk.PhotoImage(img)
        thumbnails.append(thumb)
        lbl = Label(preview_frame, image=thumb, bg="#EAF6F6")
        lbl.pack(side=LEFT, padx=5)
    
    messagebox.showinfo("Images Loaded", f"{len(files)} images selected successfully!")

def create_gif():
    if not files:
        messagebox.showwarning("Warning", "Please select images first!")
        return
    
    save_path = filedialog.asksaveasfilename(
        defaultextension=".gif",
        filetypes=[("GIF files", "*.gif")]
    )
    if not save_path:
        return
    
    duration = int(speed_slider.get())
    frames = []
    size = (400, 400)

    progress_bar['value'] = 0
    progress_bar['maximum'] = len(files)
    
    for idx, img in enumerate(files):
        frame = Image.open(img).resize(size)
        frames.append(frame)
        progress_bar['value'] = idx + 1
        root.update()  # Update progress bar
    
    frames[0].save(
        save_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0
    )

    messagebox.showinfo("✅ GIF Created",
                        f"GIF saved as:\n{os.path.basename(save_path)}\n\n"
                        f"Frames: {len(frames)}\nSpeed: {duration} ms/frame")
    progress_bar['value'] = 0

def start_gif_thread():
    threading.Thread(target=create_gif).start()

# --- Header ---
Label(root, text="GIF Maker 🎞️", font=("Arial", 22, "bold"),
      bg="#EAF6F6", fg="#0F4C75").pack(pady=20)

# --- Buttons ---
button_frame = Frame(root, bg="#EAF6F6")
button_frame.pack(pady=10)

Button(button_frame, text="🖼️ Select Images", command=select_images,
       bg="#00ADB5", fg="white", font=("Arial", 12, "bold"), width=18, bd=0).grid(row=0, column=0, padx=10)

Button(button_frame, text="🎬 Create GIF", command=start_gif_thread,
       bg="#393E46", fg="white", font=("Arial", 12, "bold"), width=18, bd=0).grid(row=0, column=1, padx=10)

# --- Speed control ---
Label(root, text="Adjust GIF Speed (ms per frame):", bg="#EAF6F6", fg="#222", font=("Arial", 11, "bold")).pack(pady=10)
speed_slider = Scale(root, from_=100, to=1000, orient=HORIZONTAL, length=300, bg="#EAF6F6", highlightthickness=0)
speed_slider.set(500)
speed_slider.pack()

# --- Image preview frame ---
Label(root, text="Preview Selected Images:", bg="#EAF6F6", fg="#0F4C75",
      font=("Arial", 11, "bold")).pack(pady=10)
preview_frame = Frame(root, bg="#EAF6F6")
preview_frame.pack(pady=5)

# --- Progress bar ---
progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, mode='determinate', length=250)
progress_bar.pack(pady=20)

# --- Footer ---
Label(root, text="Made with ❤️ in Python", bg="#EAF6F6", fg="#555",
      font=("Arial", 10, "italic")).pack(side=BOTTOM, pady=10)

root.mainloop()
