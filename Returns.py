import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Text, Scrollbar, Frame, Label, RIGHT, Y
from PIL import Image, ImageTk
import os

df = pd.read_csv("C:/Omega/Semester 4/Financial Engineering/Project/Nifty50.csv")
df.columns = df.columns.str.strip().str.replace('\n', '')

df.rename(columns={'30 D   %CHNG': '30 D %CHNG'}, inplace=True)

numeric_cols = ['30 D %CHNG', '365 D % CHNG  12-May-2023']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

df["Expected Return"] = (df["30 D %CHNG"] + df["365 D % CHNG  12-May-2023"]) / 2

root = Tk()
root.title("Expected Returns")
root.attributes('-fullscreen', True)  

background_image_path = "C:/Omega/Semester 4/Financial Engineering/Project/Returns.jpg"  # Change to your background image path
background_image = Image.open(background_image_path)
background_image = background_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

background_label = Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

value_frame = Frame(root, bg='black')
value_frame.place(relx=0.4, rely=0.2, relwidth=0.5, relheight=0.7)

def go_back():
    root.destroy()
    os.system('C:/Omega/Semester 4/Financial Engineering/Project/Frame.py')

def display_all():
    info_text.config(state='normal')
    info_text.delete('1.0', 'end')
    for index, row in df.iterrows():
        info_text.insert('end', f"Company: {row['SYMBOL']} - Expected Return: {row['Expected Return']:.2f}%\n")
    info_text.config(state='disabled')

def display_best():
    best_company = df.loc[df["Expected Return"].idxmax()]
    info_text.config(state='normal')
    info_text.delete('1.0', 'end')
    info_text.insert('end', f"Best Company to Invest In:\n"
                          f"Company: {best_company['SYMBOL']}\n"
                          f"Expected Return: {best_company['Expected Return']:.2f}%\n"
                          f"Excess Return over Risk-Free Rate: {best_company['Expected Return'] - 5:.2f}%")
    info_text.config(state='disabled')

def display_excess():
    df["Excess Return"] = df["Expected Return"] - 5
    info_text.config(state='normal')
    info_text.delete('1.0', 'end')
    for index, row in df.iterrows():
        info_text.insert('end', f"Company: {row['SYMBOL']} - Excess Return: {row['Excess Return']:.2f}%\n")
    info_text.config(state='disabled')

def display_chart():
    plt.figure(figsize=(12, 6))
    plt.bar(df["SYMBOL"], df["Expected Return"], color='skyblue')
    plt.xlabel('Company Symbol')
    plt.ylabel('Expected Return (%)')
    plt.title('Expected Returns for Each Company')
    plt.xticks(rotation=90)
    plt.tight_layout()

    for i, value in enumerate(df["Expected Return"]):
        plt.text(i, value + 0.5, f"{value:.2f}%", ha='center', va='bottom', fontsize=8)

    plt.show()

title_label = Label(root, text="EXPECTED RETURNS", font=("Algerian", 45), bg='white')
title_label.place(relx=0.5, rely=0.1, anchor="center")

button_all = Button(root, text="All Companies and Expected Returns", command=display_all, bg="#6A5ACD", font=("Arial", 14), width=30, height=2)
button_all.place(relx=0.05, rely=0.3, anchor="w")

button_best = Button(root, text="Best Company to Invest In", command=display_best, bg="#32CD32", font=("Arial", 14), width=30, height=2)
button_best.place(relx=0.05, rely=0.4, anchor="w")

button_excess = Button(root, text="Excess Return for Each Company", command=display_excess, bg="#FF6347", font=("Arial", 14), width=30, height=2)
button_excess.place(relx=0.05, rely=0.5, anchor="w")

button_chart = Button(root, text="Bar Chart", command=display_chart, bg="#1E90FF", font=("Arial", 14), width=30, height=2)
button_chart.place(relx=0.05, rely=0.6, anchor="w")

info_text = Text(value_frame, height=10, width=0, bg='black', fg='white', font=("Arial", 14), wrap='word')
info_text.pack(fill="both", expand=True, side="left")

scrollbar = Scrollbar(value_frame, command=info_text.yview, orient='vertical')
scrollbar.pack(side=RIGHT, fill=Y)
info_text.config(yscrollcommand=scrollbar.set, state='disabled')

back_button = Button(root, text="Back", command=go_back, bg="red", fg="white", font=("Arial", 14))
back_button.place(relx=0.95, rely=0.05, anchor="ne")

root.mainloop()
