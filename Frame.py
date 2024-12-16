import tkinter as tk
from tkinter import Button, Label
from PIL import Image, ImageTk
import cv2
import os

class MainApp:
    def __init__(self, master):
        self.master = master
        master.title("NIFTY50")
        master.attributes('-fullscreen', True)

        self.video_label = Label(master)
        self.video_label.pack(fill=tk.BOTH, expand=True)

        self.video_source = cv2.VideoCapture("C:/Omega/Semester 4/Financial Engineering/Project/Mframe.mp4")  

        self.update_video()

        title_label = tk.Label(master, text="NIFTY50 OPTION TRADING", font=("Algerian", 50))
        title_label.place(relx=0.5, rely=0.1, anchor="center")

        buttons_frame = tk.Frame(master, bg="#1e1e1e")  
        buttons_frame.place(relx=0.7, rely=0.5, anchor="center", relwidth=0.4)

        button_texts = ["Returns", "MACD", "Model"]
        button_commands = [self.call_returns_program, self.call_macd_program, self.call_model_program]
        button_colors = ["#FFD700", "#87CEEB", "#98FB98", "#FFA07A"]

        for text, command, color in zip(button_texts, button_commands, button_colors):
            button = Button(buttons_frame, text=text, bg=color, font=("Arial", 18), padx=20, pady=10, command=command)  
            button.pack(fill="x", padx=10, pady=5)

    def update_video(self):
        ret, frame = self.video_source.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
            img = Image.fromarray(frame_resized)
            img_tk = ImageTk.PhotoImage(image=img)
            self.video_label.config(image=img_tk)
            self.video_label.image = img_tk
        self.master.after(10, self.update_video)

    def call_returns_program(self):
        file_path = ('"C:/Omega/Semester 4/Financial Engineering/Project/Returns.py"')
        os.system(f"python {file_path}")

    def call_macd_program(self):
        file_path = ('"C:/Omega/Semester 4/Financial Engineering/Project/Macd.py"')
        os.system(f"python {file_path}")

    def call_model_program(self):
        file_path = ('"C:/Omega/Semester 4/Financial Engineering/Project/Sharpes and Treynor.py"')
        os.system(f"python {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
