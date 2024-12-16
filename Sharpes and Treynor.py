'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import tkinter as tk
import os
from tkinter import Button, Frame, Label, Text, Scrollbar, RIGHT, Y
from PIL import Image, ImageTk

class StockApp:
    def __init__(self, master):
        self.master = master
        master.title("Stock Analysis")
        master.attributes('-fullscreen', True)  

        background_image_path = "C:/Omega/Semester 4/Financial Engineering/Project/Ratio.jpg"  
        background_image = Image.open(background_image_path)
        background_image = background_image.resize((master.winfo_screenwidth(), master.winfo_screenheight()), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(background_image)

        self.background_label = Label(master, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        self.left_frame = Frame(master)
        self.left_frame.pack(side="left", padx=10, pady=10)

        self.button_avg_market = Button(master, text="Average and Standard Deviation", command=self.display_market_metrics, bg="#6A5ACD", font=("Arial", 14), width=30, height=2)
        self.button_avg_market.place(relx=0.05, rely=0.3, anchor="w")

        self.button_infy_graph = Button(master, text="Infosys", command=self.display_infy_graph, bg="#87CEEB", font=("Arial", 14), width=30, height=2)
        self.button_infy_graph.place(relx=0.05, rely=0.4, anchor="w")

        self.button_mm_graph = Button(master, text="Mahindra", command=self.display_mm_graph, bg="#90EE90", font=("Arial", 14), width=30, height=2)
        self.button_mm_graph.place(relx=0.05, rely=0.5, anchor="w")

        self.button_hindunilvr_graph = Button(master, text="Hindustan", command=self.display_hindunilvr_graph, bg="#FFA500", font=("Arial", 14), width=30, height=2)
        self.button_hindunilvr_graph.place(relx=0.05, rely=0.6, anchor="w")

        self.right_frame = Frame(master)
        self.right_frame.pack(side="right", padx=20, pady=20)

        self.metrics_label = Label(self.right_frame, text="", justify="left")
        self.metrics_label.pack()

        self.major_title = Label(master, text="MODELS", font=("Algerian", 45))
        self.major_title.pack(pady=20)


        self.results_frame = Frame(master)
        self.results_frame.pack(side="right", padx=20, pady=20)

        self.info_label = Label(self.results_frame, text="", bg='black', fg='white', font=("Arial", 14), wraplength=400, justify="right")
        self.info_label.pack(fill="both", expand=True, side="right")

        self.download_data()

        self.back_button = Button(master, text="Back", command=self.go_back, bg="red", fg="white", font=("Arial", 14))
        self.back_button.place(relx=0.95, rely=0.05, anchor="ne")

    def go_back(self):
        self.master.destroy()
        os.system('C:/Omega/Semester 4/Financial Engineering/Project/Frame.py')

    def download_data(self):
        self.nifty_data = yf.download('^NSEI', start='2023-05-15', end='2024-05-15')['Adj Close']
        
        self.infy_data = yf.download('INFY.NS', start='2023-05-15', end='2024-05-15')['Adj Close']
        self.mm_data = yf.download('M&M.NS', start='2023-05-15', end='2024-05-15')['Adj Close']
        self.hindunilvr_data = yf.download('HINDUNILVR.NS', start='2023-05-15', end='2024-05-15')['Adj Close']

    def display_market_metrics(self):
        market_avg_return = self.nifty_data.pct_change().mean()

        market_std_dev = self.nifty_data.pct_change().std()

        self.info_label.config(text=f"Average Market Return: {market_avg_return}\n"
                                        f"Market Standard Deviation: {market_std_dev}")

    def display_infy_graph(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.infy_data.index, self.infy_data)
        plt.xlabel('Date')
        plt.ylabel('Infosys Price')
        plt.title('Infosys Stock Prices')
        plt.legend()
        plt.show()

        infy_returns = self.infy_data.pct_change().dropna()
        nifty_returns = self.nifty_data.pct_change().dropna()

        covariance_infy = np.cov(infy_returns, nifty_returns)[0, 1]
        market_var = np.var(nifty_returns)

        beta_infy = covariance_infy / market_var

        risk_free_rate = 0.05  
        excess_returns_infy = infy_returns - risk_free_rate

        sharpe_ratio_infy = excess_returns_infy.mean() / excess_returns_infy.std()

        treynor_ratio_infy = excess_returns_infy.mean() / beta_infy

        self.info_label.config(text=f"Infosys Metrics:\n"
                                        f"Beta: {beta_infy}\n"
                                        f"Sharpe's Ratio: {sharpe_ratio_infy}\n"
                                        f"Treynor's Ratio: {treynor_ratio_infy}")

    def display_mm_graph(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.mm_data.index, self.mm_data, label='M&M', color='green')
        plt.xlabel('Date')
        plt.ylabel('M&M Price')
        plt.title('M&M Stock Prices')
        plt.legend()
        plt.show()

        mm_returns = self.mm_data.pct_change().dropna()
        nifty_returns = self.nifty_data.pct_change().dropna()

        covariance_mm = np.cov(mm_returns, nifty_returns)[0, 1]
        market_var = np.var(nifty_returns)

        beta_mm = covariance_mm / market_var

        risk_free_rate = 0.05  
        excess_returns_mm = mm_returns - risk_free_rate

        sharpe_ratio_mm = excess_returns_mm.mean() / excess_returns_mm.std()

        treynor_ratio_mm = excess_returns_mm.mean() / beta_mm

        self.info_label.config(text=f"M&M Metrics:\n"
                                        f"Beta: {beta_mm}\n"
                                        f"Sharpe's Ratio: {sharpe_ratio_mm}\n"
                                        f"Treynor's Ratio: {treynor_ratio_mm}")

    def display_hindunilvr_graph(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.hindunilvr_data.index, self.hindunilvr_data, label='HINDUNILVR', color='orange')
        plt.xlabel('Date')
        plt.ylabel('HINDUNILVR Price')
        plt.title('HINDUNILVR Stock Prices')
        plt.legend()
        plt.show()

        hindunilvr_returns = self.hindunilvr_data.pct_change().dropna()
        nifty_returns = self.nifty_data.pct_change().dropna()

        covariance_hindunilvr = np.cov(hindunilvr_returns, nifty_returns)[0, 1]
        market_var = np.var(nifty_returns)

        beta_hindunilvr = covariance_hindunilvr / market_var

        risk_free_rate = 0.05 
        excess_returns_hindunilvr = hindunilvr_returns - risk_free_rate

        sharpe_ratio_hindunilvr = excess_returns_hindunilvr.mean() / excess_returns_hindunilvr.std()

        treynor_ratio_hindunilvr = excess_returns_hindunilvr.mean() / beta_hindunilvr

        self.info_label.config(text=f"HINDUNILVR Metrics:\n"
                                        f"Beta: {beta_hindunilvr}\n"
                                        f"Sharpe's Ratio: {sharpe_ratio_hindunilvr}\n"
                                        f"Treynor's Ratio: {treynor_ratio_hindunilvr}")


root = tk.Tk()
app = StockApp(root)
root.mainloop()


import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import tkinter as tk
from tkinter import Button, Frame, Label, Listbox, Scrollbar, RIGHT, Y
from PIL import Image, ImageTk

class StockApp:
    def __init__(self, master):
        self.master = master
        master.title("Stock Analysis")
        master.attributes('-fullscreen', True)

        background_image_path = "C:/Omega/Semester 4/Financial Engineering/Project/Ratio.jpg"
        background_image = Image.open(background_image_path)
        background_image = background_image.resize((master.winfo_screenwidth(), master.winfo_screenheight()), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(background_image)

        self.background_label = Label(master, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        self.left_frame = Frame(master)
        self.left_frame.pack(side="left", padx=10, pady=10)

        self.button_avg_market = Button(master, text="Average and Standard Deviation", command=self.display_market_metrics, bg="#6A5ACD", font=("Arial", 14), width=30, height=2)
        self.button_avg_market.place(relx=0.05, rely=0.3, anchor="w")

        self.right_frame = Frame(master)
        self.right_frame.pack(side="right", padx=20, pady=20)

        self.metrics_label = Label(self.right_frame, text="", justify="left")
        self.metrics_label.pack()

        self.major_title = Label(master, text="MODELS", font=("Algerian", 45))
        self.major_title.pack(pady=20)

        self.results_frame = Frame(master)
        self.results_frame.pack(side="right", padx=20, pady=20)

        self.info_label = Label(self.results_frame, text="", bg='black', fg='white', font=("Arial", 14), wraplength=400, justify="right")
        self.info_label.pack(fill="both", expand=True, side="right")

        self.back_button = Button(master, text="Back", command=self.go_back, bg="red", fg="white", font=("Arial", 14))
        self.back_button.place(relx=0.95, rely=0.05, anchor="ne")

        self.create_company_listbox()

        self.download_data()

    def create_company_listbox(self):
        self.company_listbox = Listbox(self.left_frame, selectmode=tk.SINGLE, font=("Arial", 14), width=30, height=20)
        self.company_listbox.pack(side="left", fill="y")
        scrollbar = Scrollbar(self.left_frame, orient="vertical")
        scrollbar.config(command=self.company_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.company_listbox.config(yscrollcommand=scrollbar.set)

        self.company_listbox.bind("<<ListboxSelect>>", self.on_company_select)

        self.load_company_list()

    def load_company_list(self):
        # Assuming you have a CSV with the symbols and names of Nifty 50 companies
        self.nifty_50_companies = pd.read_csv('C:/Omega/Semester 4/Financial Engineering/Project/Nifty50.csv')
        for index, row in self.nifty_50_companies.iterrows():
            self.company_listbox.insert(tk.END, row['Company'])

    def on_company_select(self, event):
        selected_index = self.company_listbox.curselection()[0]
        selected_symbol = self.nifty_50_companies.iloc[selected_index]['Symbol']
        selected_company = self.nifty_50_companies.iloc[selected_index]['Company']
        self.display_company_metrics(selected_symbol, selected_company)

    def go_back(self):
        self.master.destroy()
        os.system('C:/Omega/Semester 4/Financial Engineering/Project/Frame.py')

    def download_data(self):
        self.nifty_data = yf.download('^NSEI', start='2023-05-15', end='2024-05-15')['Adj Close']
        self.stock_data = {}

        for index, row in self.nifty_50_companies.iterrows():
            symbol = row['Symbol']
            self.stock_data[symbol] = yf.download(f'{symbol}.NS', start='2023-05-15', end='2024-05-15')['Adj Close']

    def display_market_metrics(self):
        market_avg_return = self.nifty_data.pct_change().mean()
        market_std_dev = self.nifty_data.pct_change().std()

        self.info_label.config(text=f"Average Market Return: {market_avg_return}\n"
                                    f"Market Standard Deviation: {market_std_dev}")

    def display_company_metrics(self, symbol, company_name):
        data = self.stock_data[symbol]

        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data, label=company_name)
        plt.xlabel('Date')
        plt.ylabel(f'{company_name} Price')
        plt.title(f'{company_name} Stock Prices')
        plt.legend()
        plt.show()

        company_returns = data.pct_change().dropna()
        nifty_returns = self.nifty_data.pct_change().dropna()

        covariance = np.cov(company_returns, nifty_returns)[0, 1]
        market_var = np.var(nifty_returns)

        beta = covariance / market_var

        risk_free_rate = 0.05
        excess_returns = company_returns - risk_free_rate

        sharpe_ratio = excess_returns.mean() / excess_returns.std()
        treynor_ratio = excess_returns.mean() / beta

        self.info_label.config(text=f"{company_name} Metrics:\n"
                                    f"Beta: {beta}\n"
                                    f"Sharpe's Ratio: {sharpe_ratio}\n"
                                    f"Treynor's Ratio: {treynor_ratio}")

root = tk.Tk()
app = StockApp(root)
root.mainloop()

final
import tkinter as tk
from tkinter import Label, ttk
import os
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

class StockApp:
    def __init__(self, master):
        self.master = master
        master.title("Stock Analysis")
        master.attributes('-fullscreen', True)  

        background_image_path = "C:/Omega/Semester 4/Financial Engineering/Project/Ratio.jpg"  
        background_image = Image.open(background_image_path)
        background_image = background_image.resize((master.winfo_screenwidth(), master.winfo_screenheight()), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(background_image)

        self.background_label = tk.Label(master, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        self.dropdown = ttk.Combobox(master, state="readonly", width=80)
        self.dropdown.place(relx=0.3, rely=0.29, anchor="w")

        self.dropdown["values"] = [
            "ADANIENT", "M&M", "HEROMOTOCO", "ONGC", "LT", "JSWSTEEL", "HINDALCO", "ADANIPORTS", 
            "EICHERMOT", "SUNPHARMA", "NTPC", "RELIANCE", "INDUSINDBK", "ULTRACEMCO", "SBIN", 
            "TITAN", "WIPRO", "SHRIRAMFIN", "TECHM", "COALINDIA", "MARUTI", "LTIM", "POWERGRID", 
            "BAJAJ-AUTO", "SBILIFE", "APOLLOHOSP", "TATASTEEL", "TATAMOTORS", "HCLTECH", "HDFCBANK", 
            "KOTAKBANK", "HDFCLIFE", "INFY", "BPCL", "BHARTIARTL", "BRITANNIA", "BAJAJFINSV", "GRASIM", 
            "HINDUNILVR", "DIVISLAB", "ASIANPAINT", "ITC", "BAJFINANCE", "DRREDDY", "ICICIBANK", "AXISBANK", 
            "NESTLEIND", "TATACONSUM", "TCS", "CIPLA"
        ]

        self.dropdown.bind("<<ComboboxSelected>>", self.fetch_data)

        self.right_frame = tk.Frame(master)
        self.right_frame.pack(side="left", padx=20, pady=20)

        self.major_title = Label(master, text="MODELS", font=("Algerian", 45))
        self.major_title.pack(pady=50)

        self.info_label = tk.Label(self.right_frame, text="", bg='black', fg='white', font=("Arial", 14), wraplength=400, justify="right")
        self.info_label.pack(fill="both", expand=True, side="right")

        self.back_button = tk.Button(master, text="Back", command=self.go_back, bg="red", fg="white", font=("Arial", 14))
        self.back_button.place(relx=0.95, rely=0.05, anchor="ne")

    def go_back(self):
        self.master.destroy()
        os.system('C:/Omega/Semester 4/Financial Engineering/Project/Frame.py')

    def fetch_data(self, event):
        selected_company = self.dropdown.get()
        data = yf.download(selected_company + ".NS", start='2023-05-15', end='2024-05-15')['Adj Close']
        
        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data, label=selected_company)
        plt.xlabel('Date')
        plt.ylabel(f'{selected_company} Price')
        plt.title(f'{selected_company} Stock Prices')
        plt.legend()
        plt.show()

        returns = data.pct_change().dropna()
        nifty_data = yf.download('^NSEI', start='2023-05-15', end='2024-05-15')['Adj Close']
        nifty_returns = nifty_data.pct_change().dropna()

        covariance = np.cov(returns, nifty_returns)[0, 1]
        market_var = np.var(nifty_returns)

        beta = covariance / market_var

        risk_free_rate = 0.05
        excess_returns = returns - risk_free_rate

        sharpe_ratio = excess_returns.mean() / excess_returns.std()

        treynor_ratio = excess_returns.mean() / beta

        self.info_label.config(text=f"{selected_company} Metrics:\n"
                                     f"Beta: {beta}\n"
                                     f"Sharpe's Ratio: {sharpe_ratio}\n"
                                     f"Treynor's Ratio: {treynor_ratio}")

 self.right_frame = tk.Frame(master)
        self.right_frame.pack(pady=20)
root = tk.Tk()
app = StockApp(root)
root.mainloop()


'''
import tkinter as tk
from tkinter import Label, ttk
import os
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

class StockApp:
    def __init__(self, master):
        self.master = master
        master.title("Stock Analysis")
        master.attributes('-fullscreen', True)  

        background_image_path = "C:/Omega/Semester 4/Financial Engineering/Project/Ratio.jpg"  
        background_image = Image.open(background_image_path)
        background_image = background_image.resize((master.winfo_screenwidth(), master.winfo_screenheight()), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(background_image)

        self.background_label = tk.Label(master, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        self.major_title = Label(master, text="MODELS", font=("Algerian", 45))
        self.major_title.pack(pady=50)

        self.dropdown = ttk.Combobox(master, state="readonly", width=40)
        self.dropdown.place(relx=0.5, rely=0.35, anchor="center")
        self.dropdown["values"] = [
            "ADANIENT", "M&M", "HEROMOTOCO", "ONGC", "LT", "JSWSTEEL", "HINDALCO", "ADANIPORTS", 
            "EICHERMOT", "SUNPHARMA", "NTPC", "RELIANCE", "INDUSINDBK", "ULTRACEMCO", "SBIN", 
            "TITAN", "WIPRO", "SHRIRAMFIN", "TECHM", "COALINDIA", "MARUTI", "LTIM", "POWERGRID", 
            "BAJAJ-AUTO", "SBILIFE", "APOLLOHOSP", "TATASTEEL", "TATAMOTORS", "HCLTECH", "HDFCBANK", 
            "KOTAKBANK", "HDFCLIFE", "INFY", "BPCL", "BHARTIARTL", "BRITANNIA", "BAJAJFINSV", "GRASIM", 
            "HINDUNILVR", "DIVISLAB", "ASIANPAINT", "ITC", "BAJFINANCE", "DRREDDY", "ICICIBANK", "AXISBANK", 
            "NESTLEIND", "TATACONSUM", "TCS", "CIPLA"
        ]
        self.dropdown.config(foreground="black")
        
        self.right_frame = tk.Frame(master)
        self.right_frame.place(relx=0.5, rely=0.55, anchor="center")


        self.dropdown.bind("<<ComboboxSelected>>", self.fetch_data)

        
        self.info_label = tk.Label(self.right_frame, text="", bg='black', fg='white', font=("Arial", 14), wraplength=400, justify="right")
        self.info_label.pack(fill="both", expand=True)

        self.back_button = tk.Button(master, text="Back", command=self.go_back, bg="red", fg="white", font=("Arial", 14))
        self.back_button.place(relx=0.95, rely=0.05, anchor="ne")

        

    def go_back(self):
        self.master.destroy()
        os.system('C:/Omega/Semester 4/Financial Engineering/Project/Frame.py')

    def fetch_data(self, event):
        selected_company = self.dropdown.get()
        data = yf.download(selected_company + ".NS", start='2023-05-15', end='2024-05-15')['Adj Close']
        
        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data, label=selected_company)
        plt.xlabel('Date')
        plt.ylabel(f'{selected_company} Price')
        plt.title(f'{selected_company} Stock Prices')
        plt.legend()
        plt.show()

        returns = data.pct_change().dropna()
        nifty_data = yf.download('^NSEI', start='2023-05-15', end='2024-05-15')['Adj Close']
        nifty_returns = nifty_data.pct_change().dropna()

        covariance = np.cov(returns, nifty_returns)[0, 1]
        market_var = np.var(nifty_returns)

        beta = covariance / market_var

        risk_free_rate = 0.08
        excess_returns = returns - risk_free_rate

        sharpe_ratio = excess_returns.mean() / excess_returns.std()

        treynor_ratio = excess_returns.mean() / beta

        self.info_label.config(text=f"{selected_company} Metrics:\n"
                                     f"Beta: {beta}\n"
                                     f"Sharpe's Ratio: {sharpe_ratio}\n"
                                     f"Treynor's Ratio: {treynor_ratio}")
        
        self.info_label.pack_forget()  # Remove previous placement

        self.info_label.pack(side="top", padx=20, pady=10)  # Place below the combo box


root = tk.Tk()
app = StockApp(root)
root.mainloop()
