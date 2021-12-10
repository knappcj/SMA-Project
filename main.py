import random as rd
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import tkinter as tk
import matplotlib.figure as fig
import matplotlib.backends.backend_tkagg as bac
from SMA import TradingStrategy
from find_max import findMax
from buy_sell import buySell

# 1.The user can enter the day range (such as 2020-01-01 to 2021-09-01)
# 2. The user can also choose the industry from the stocks in S&P 500 index within the day range and the industry:
# 3. Your code will find a portfolio of two stocks that generates the best SMA trading strategy that generate
# the highest profits (price vs. SMA)
# 4. The portfolio has a $50,000 in each stock for a total of $100,000 at the beginning of the day range
# 5. Your code will need to find the best N-day in the N-day SMA for each stock’s trading strategy
# 6. At the end, your code displays each transaction (buy or sell on what day) and the total profit
# 7. Each transaction is to buy or sell your entire holding of that stock

industry_dict = {}
industry_list = []
def loadDict():
    stock_list = pd.read_csv('sp500.csv')
    tickers = stock_list['Ticker']
    industries = stock_list['Industry']
    for i in stock_list.index:
        industry_dict[tickers[i]] = industries[i]
    for i in industries:
        if i not in industry_list:
            industry_list.append(i)
    industry_list.sort()
    return

def findBest(industry, begin_day, end_day):
    results_dict = {}
    for i in industry_dict:
        if industry_dict[i] == industry:
            try:
                results_dict[i] = TradingStrategy(yf.download(i, begin_day, end_day))
            except:
                print("Could not find data for ",i)
    best_tickers, best_day = findMax(results_dict)
    ticker1 = best_tickers[0]
    ticker2 = best_tickers[1]
    buySell1, return1 = buySell(ticker1, begin_day, end_day, best_day)
    buySell2, return2 = buySell(ticker2, begin_day, end_day, best_day)
    instruct1 = buySellDates(buySell1,ticker1)
    instruct2 = buySellDates(buySell2, ticker2)
    return ticker1, ticker2, instruct1, instruct2, return1, return2, best_day


def buySellDates(data, ticker):
    instructions = []
    for i in data.index:

        if data.loc[i, 'Buy or Sell'] >= 1:
            s = 'Sell '+ ticker+ " on "+ str(i)[0:10]
            instructions.append(s)
        if data.loc[i, 'Buy or Sell'] <= -1:
            s = 'Buy ' + ticker + " on " + str(i)[0:10]
            instructions.append(s)
    return instructions


def SetSelect():
    # +++your code here+++
    # Clear the window and reset the values to be displayed
    myselect.delete(0, tk.END)
    for i in industry_list:
        myselect.insert(tk.END, i)
    # +++your code here+++
    return

def runFunc():
    myanswer1.delete(0, tk.END)
    myanswer2.delete(0, tk.END)
    selectedid = industry_list[myselect.curselection()[0]]
    start = begindate.get()
    end = enddate.get()
    print(selectedid)
    tick1, tick2, ans1, ans2, r1, r2,bestDay = findBest(str(selectedid), str(start), str(end))
    format1 = "${:,.2f}".format(r1)
    format2 = "${:,.2f}".format(r2)
    formatp1 ="{:.2%}".format(r1/50000)
    formatp2 ="{:.2%}".format(r2/50000)
    myanswer1.insert(tk.END, 'SMA Days: '+ str(bestDay))
    myanswer2.insert(tk.END, 'SMA Days: '+ str(bestDay))
    myanswer1.insert(tk.END, 'TICKER: ' + tick1)
    myanswer1.insert(tk.END, 'Return: ' + format1)
    myanswer2.insert(tk.END, 'TICKER: ' + tick2)
    myanswer2.insert(tk.END, 'Return:' + format2)
    myanswer1.insert(tk.END, 'Percent Return: ' + formatp1)
    myanswer2.insert(tk.END, 'Percent Return: ' + formatp2)
    for i in ans1:
        myanswer1.insert(tk.END, i)
    for i in ans2:
        myanswer2.insert(tk.END, i)




#TKinter window



mywindow = tk.Tk()
mywindow.geometry('800x400')
mywindow.title('Project #1 - Christopher Knapp')

myframe = tk.Frame(mywindow)
myframe.pack(side = tk.RIGHT)
myscroll = tk.Scrollbar(myframe, orient=tk.VERTICAL)
myselect = tk.Listbox(myframe, yscrollcommand=myscroll.set)
myanswer1 = tk.Listbox(myframe, yscrollcommand=myscroll.set)
myanswer2 = tk.Listbox(myframe, yscrollcommand=myscroll.set)
myselect.pack(side=tk.LEFT)
myanswer1.pack(side=tk.LEFT)
myanswer2.pack(side=tk.LEFT)
myscroll.config(command=myselect.yview)
myscroll.pack(side=tk.RIGHT, fill=tk.Y)

loadDict()
SetSelect()

tk.Label(mywindow, text = 'Begin Date').place(x=30, y=50)
begindate = tk.StringVar()
tk.Entry(mywindow, textvariable = begindate).place(x=100, y=50)

tk.Label(mywindow, text = 'End Date').place(x=300, y=50)
enddate = tk.StringVar()
tk.Entry(mywindow, textvariable = enddate).place(x=370, y=50)

tk.Button(mywindow,text="Find Best Two", command = runFunc).place(x= 250, y=300)

intructLabel = tk.Label(mywindow, text = 'Select Industry Here ->').place(x=80, y=200)
dateLabel = tk.Label(mywindow, text = 'Input date as YYYY-MM-DD').place(x=30, y=10)

mywindow.mainloop()


