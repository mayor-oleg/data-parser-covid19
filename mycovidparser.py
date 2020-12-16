# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 21:50:10 2020

@author: jr
"""
# Base import
import pandas as pd
import time
from datetime import date
from datetime import timedelta
# Error exeptions import
from urllib.error import URLError
from urllib.error import HTTPError

dates = date(2020,1,22)
today = date.today()

# Block for receive Data 
def parsercovid(d=None):
    
    z=0
                
    while today > dates:
        if  today == (dates+timedelta(z+1)):
            print ('There is no data for today', today)
            return
        l = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'+str((dates+timedelta(z)).strftime("%m-%d-%Y"))+'.csv'
        print ('loading data from: ' , (dates+timedelta(z)))
        
#Control exeptions
        tries = 5
        for i in range(tries):
            try:
                db = pd.read_csv(l)
                #print (db)
            except (HTTPError, URLError):
                if today == (dates+timedelta(z+1)):
                    print ("There is night in your country.")
                    print ("And there is no Data for 2 last date.")
                    break
            except URLError as e:
                if i < tries-1 : # i is zero indexed
                    time.sleep(3)
                    print ("Connection problems", i+1, "try" )
                    print (e)
                    continue
                else:
                    msg = "there is big problem to get the Data, stop trying"
                    print (msg)
                    raise 
            break
        
            
        db['Date'] = (dates+timedelta(z)).strftime("%m-%d-%Y")
        db.set_index(['Date', db.index], inplace=True )
        
        df_name = db.columns.to_list()
        if 'Active'not in df_name:
            db['Active'] = 0
# Clean Data            
        for name in df_name:
            if "Country" in name:
                db.rename(columns={name:'Country'}, inplace = True)
            if "State" in name:
                db.rename(columns={name:'State'}, inplace = True)
        db.loc[db['Country'] == 'Mainland China', 'Country']='China'    
        df = pd.DataFrame(db[['State','Country','Confirmed','Recovered','Deaths','Active']])
        df.fillna(0)
        #print(df)
        yield df.fillna(0)
        
        z+=1
#See each DF of each Day 
#for df in parsercovid(dates):
    #print (df)
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()    