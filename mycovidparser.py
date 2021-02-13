# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 21:50:10 2020

@author: jr
"""

import pandas as pd
from datetime import date
from datetime import timedelta
from urllib.error import URLError
from urllib.error import HTTPError
import time

dates = date(2020,1,22)
today = date.today()


def parsercovid(d):
    
    z=0
    while today > d:
        if  today == d+timedelta(z):
            print ('There is no data for today', today)
            return
        l = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'+str((d+timedelta(z)).strftime("%m-%d-%Y"))+'.csv'
        print ('loading data from: ' , (d+timedelta(z)))
        

        tries = 5
        for i in range(tries):
            try:
                db = pd.read_csv(l)
                #print (db)
            except (HTTPError, URLError):
                if today == d:
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
        
            
        db['Date'] = (d+timedelta(z)).strftime("%m-%d-%Y")
        db.set_index(['Date', db.index], inplace=True )
        
        df_name = db.columns.to_list()
        if 'Active'not in df_name:
            db['Active'] = 0
            
        for name in df_name:
            if "Country" in name:
                db.rename(columns={name:'Country'}, inplace = True)
            if "State" in name:
                db.rename(columns={name:'State'}, inplace = True)
        db.loc[db['Country'] == 'Mainland China', 'Country']='China' 
        db.loc[db['Country'] == 'Taiwan*']='Taiwan'
        df = pd.DataFrame(db[['State','Country','Confirmed','Recovered','Deaths','Active']])
        df.fillna(0)
        #print(df)
        yield df.fillna(0)
        
        z+=1
#for df in parsercovid(dates):
    #print (df)
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()    
