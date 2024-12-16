import pandas as pd
import ta
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import Button, Frame, Label, Text, Scrollbar, RIGHT, Y
from PIL import Image, ImageTk
import os

class MacdApp:
    def __init__(self, master):
        self.master = master
        master.title("MOVING AVERAGE CONVERGENCE AND DIVERGENCE")
        master.attributes('-fullscreen', True)  

        background_image_path = "C:/Omega/Semester 4/Financial Engineering/Project/Ratio.jpg"  # Change to your background image path
        background_image = Image.open(background_image_path)
        background_image = background_image.resize((master.winfo_screenwidth(), master.winfo_screenheight()), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(background_image)

        self.background_label = Label(master, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        title_label = Label(master, text="MOVING AVERAGE CONVERGENCE AND DIVERGENCE", font=("Algerian", 45), bg='white')
        title_label.place(relx=0.5, rely=0.1, anchor="center")

        self.left_frame = Frame(master, bg='black')
        self.left_frame.place(relx=0.1, rely=0.5, anchor='w')

        self.button_values = Button(self.left_frame, text="Values", command=self.display_values, bg="#6A5ACD", fg="white", font=("Arial", 14), width=10, height=2)
        self.button_values.pack(side="top", padx=10, pady=5)

        self.button_graph = Button(self.left_frame, text="Graph", command=self.display_graph, bg="#87CEEB", fg="white", font=("Arial", 14), width=10, height=2)
        self.button_graph.pack(side="top", padx=10, pady=5)

        self.right_frame = Frame(master, bg='black')
        self.right_frame.place(relx=0.5, rely=0.6, anchor='w')

        self.info_text = Text(self.right_frame, height=30, width=50, bg='black', fg='white', font=("Arial", 12), wrap='word')
        self.info_text.pack(fill="both", expand=True, side="left")

        self.scrollbar = Scrollbar(self.right_frame, command=self.info_text.yview, orient='vertical')
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.info_text.config(yscrollcommand=self.scrollbar.set)

        self.back_button = Button(master, text="Back", command=self.go_back, bg="red", fg="white", font=("Arial", 14))
        self.back_button.place(relx=0.95, rely=0.2, anchor="ne")

    def go_back(self):
        self.master.destroy()
        os.system('C:/Omega/Semester 4/Financial Engineering/Project/Frame.py')
        

    def display_values(self):
        df = pd.read_csv("C:/Omega/Semester 4/Financial Engineering/Project/Nifty50.csv")
        df.columns = df.columns.str.strip().str.replace('\n', '')

        df.rename(columns={'30 D   %CHNG': 'CLOSE'}, inplace=True)

        numeric_cols = ['CLOSE']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

        df['macd'] = ta.trend.macd(df['CLOSE'], window_fast=12, window_slow=26)

        df['macd_signal'] = ta.trend.macd_signal(df['CLOSE'], window_fast=12, window_slow=26, window_sign=9)

        df['macd_histogram'] = df['macd'] - df['macd_signal']

        self.info_text.delete(1.0, tk.END)  # Clear previous text
        self.info_text.insert(tk.END, df[['SYMBOL', 'macd', 'macd_signal', 'macd_histogram']])

    def display_graph(self):
        df = pd.read_csv("C:/Omega/Semester 4/Financial Engineering/Project/Nifty50.csv")
        df.columns = df.columns.str.strip().str.replace('\n', '')

        df.rename(columns={'30 D   %CHNG': 'CLOSE'}, inplace=True)

        numeric_cols = ['CLOSE']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

        df['macd'] = ta.trend.macd(df['CLOSE'], window_fast=12, window_slow=26)

        df['macd_signal'] = ta.trend.macd_signal(df['CLOSE'], window_fast=12, window_slow=26, window_sign=9)

        plt.figure(figsize=(12, 6))
        plt.plot(df['macd'], color='green', label='MACD')
        plt.plot(df['macd_signal'], color='red', label='Signal Line')
        plt.bar(df.index, df['macd'] - df['macd_signal'], color='skyblue', label='Histogram')
        plt.xlabel('Index')
        plt.ylabel('Values')
        plt.title('MACD, Signal Line, and Histogram', fontdict={"fontname": "Algerian", "fontsize": 20})
        plt.legend()
        plt.grid(True)
        plt.show(block=False)

root = tk.Tk()
app = MacdApp(root)
root.mainloop()
