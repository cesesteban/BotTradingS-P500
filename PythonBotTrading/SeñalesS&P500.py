# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 04:39:18 2021

@author: c-est
"""

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt
import time
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

j=0
dayCondition=True
while dayCondition:

    pd.options.mode.chained_assignment=None    
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tickers = pd.read_html(url, flavor='html5lib')[0]
    tickers = tickers.Symbol.to_list()
    tickers = [i.replace('.','-') for i in tickers]
    start="2021-02-01"
    interval="1h"
    
    def AddDirectory():
        import os
        path='C:/Users/c-est/Desktop/botTrading'    
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)
        
    def RemoveDirectory():
        import shutil
        path = 'C:/Users/c-est/Desktop/botTrading'    
        
        try:
            shutil.rmtree(path)
        except OSError:
            print ("Deletion of the directory %s failed" % path)
        else:
            print ("Successfully deleted the directory %s" % path)
        
    def Chart(stock,start,interval):
        ticker=yf.Ticker(stock)
        now=dt.datetime.now()
        path='C:/Users/c-est/Desktop/botTrading/chart'
        stock_historical=ticker.history(start=start, end=now, interval=interval)    
        adj_close_px=stock_historical['Close']
        stock_historical['21'] = adj_close_px.rolling(window=21).mean()
        stock_historical['55'] = adj_close_px.rolling(window=55).mean()
        stock_historical['150'] = adj_close_px.rolling(window=150).mean()
        stock_historical[['Close', '21', '55', '150']].plot()
        plt.savefig(path+str(stock)+'.png')
    
    def TradingStrategie(stock,start,interval):   
        df = yf.download(stock, start=start, interval=interval, threads=False)   
        df['MA21']=df['Adj Close'].rolling(window=21).mean()
        df['MA55']=df['Adj Close'].rolling(window=55).mean()
        df['MA150']=df['Adj Close'].rolling(window=150).mean()    
        df["MA21"].fillna(0, inplace = True)
        df["MA55"].fillna(0, inplace = True)
        df["MA150"].fillna(0, inplace = True)    
        df.loc[(df['MA21'] > df['MA55']) & (df['MA55'] > df['MA150']) & (df['Adj Close'] > df['MA21']),'Signal']= 'Buy'
        df.loc[(df['Adj Close'] < df['MA21']), 'Signal']= 'Sell'
        df['Signal'].fillna('Wait and see', inplace = True)        
        return df
    
    def sendemail(stock, message):                
        user="tradingalerta51@gmail.com"
        password="TradingAlerta51+"
        to=["c-esteban@live.com","ces.esteban@gmail.com","fmaxilamas@gmail.com","hectorces@yahoo.com.ar","todoimprimimos@gmail.com","leo.unlp@live.com","guzmfernando@gmail.com","rubenvega1994@gmail.com","leonardo158xd@gmail.com","pjsanchez197@gmail.com"]
        subject="Alert!"
        message=message
        path='C:/Users/c-est/Desktop/botTrading/chart'
        file=path+str(stock)+'.png'
        
        gmail=smtplib.SMTP('smtp.gmail.com', 587)
        gmail.starttls()
        
        gmail.login(user,password)
        gmail.set_debuglevel(1)
        
        header=MIMEMultipart()
        header['Subject']=subject
        header['From']=user
        header['To'] =', '.join(to)
        
        message=MIMEText(message, 'plain')
        header.attach(message)
        
        if(os.path.isfile(file)):
            attch=MIMEBase('application', 'octet-stream')
            attch.set_payload(open(file,'rb').read())
            encode_base64(attch)
            attch.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
            header.attach(attch)
        
        gmail.sendmail(user, to, header.as_string())
        gmail.quit()
        print('OK!')
        
    AddDirectory()
    
    i=0
    condition=True
    while condition: 
        try:        
            stock=tickers[i]    
            print(stock)    
            signal=TradingStrategie(stock,start,interval)['Signal']
            if (signal[len(signal)-1])!=(signal[len(signal)-2]):
                if (signal[len(signal)-1]=='Buy') & (signal[len(signal)-2]=='Sell'):
                    Chart(stock,start,interval)
                    message="TestBot-price above average, recommendation buy: "+ str(stock)
                    sendemail(stock, message)
                elif (signal[len(signal)-1]=='Sell') & (signal[len(signal)-2]=='Buy'):
                    Chart(stock,start,interval)
                    message="TestBot-price below average, recommendation close position: "+ str(stock)
                    sendemail(stock, message)
            i=i+1
            if i==504:
                condition=False
            time.sleep(0.01)
        except Exception as e:
            print('ERROR', e)
            i=i-1
            pass
    
    RemoveDirectory()
            
    print('-------------Finish------------')
    
    j=j+1
    if j==5:
        dayCondition=False
    time.sleep(3600)
    
    
    
'--------------------------------------------------------------------'
    
'''for stock in tickers:
    try:
        print(stock)
        signal=TradingStrategie(stock,start,interval)['Signal']
        if (signal[len(signal)-1])!=(signal[len(signal)-2]):
            if (signal[len(signal)-1]=='Buy') & (signal[len(signal)-2]=='Sell'):
                print("Open position long: ", stock)
                Chart(stock,start,interval)
            elif (signal[len(signal)-1]=='Sell') & (signal[len(signal)-2]=='Buy'):
                print("Close position long: ", stock)
                Chart(stock,start,interval)
        time.sleep(0.01)
    except Exception as e:
        print('ERROR', e)
        pass

print('-------------Finish------------')'''
    
'''stock='FE'
Chart(stock,start,interval)
TradingStrategie(stock,start,interval)'''
    





