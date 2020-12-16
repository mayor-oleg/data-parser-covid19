# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 20:31:45 2020

@author: jr
"""
#My imports
from mycovidparser import parsercovid as parser
#Base import
import pandas as pd
from datetime import date
from datetime import timedelta
import numpy as np





def count_new_infected(country,parser):
    
    perday = []
    inf = 0
    s= 0
    x=0
    date = []
    infected = [0]
    df_pred = pd.DataFrame()
    for df in parser():
        newdf = df.loc[df['Country'] == country]
        if newdf.empty:
            columns = ['State', 'Country', 'Confirmed', 'Recovered', 'Deaths', 'Active']
            newdf = pd.DataFrame(np.zeros(df.shape), columns = columns)
            newdf['Country'] = country
            work_newdf = newdf.groupby(['Country']).sum()
            work_newdf['Date'] = df.index[0][0]
            df_pred = pd.concat([df_pred, work_newdf[['Confirmed',  'Recovered',  'Deaths',  'Active','Date']]])#,ignore_index=True)
            s = 0
            perday.append(s)
            date.append((df.index[0])[0])
        
        else:
            
            work_newdf = newdf.groupby(['Country']).sum()
            work_newdf['Date'] = df.index[0][0]
            df_pred = pd.concat([df_pred, work_newdf[['Confirmed',  'Recovered',  'Deaths',  'Active','Date']]])#,ignore_index=True)
            s = work_newdf['Confirmed'].sum() 
            perday.append(s)
            date.append((df.index[0])[0])
            x +=1
    #print (len(df_pred)) #Df with out new infected
    x=1
    while x < len(perday):
        if perday[x] == perday[x-1]:
            infected.append(inf)
        else:
            inf = abs(perday[x]-perday[x-1])
            infected.append(inf)
        x+=1
    #print (infected) #new infected this line for test
    #print (len(infected)) #How many days from start
    df_pred['New_infected'] = infected
    df_pred.to_csv('df_pred'+country[:5]+'.csv')
    return df_pred
    
#All countries - not recomend for test too much time
def country_list():
    today = date.today()
    l = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'+((today-timedelta(5)).strftime("%m-%d-%Y"))+'.csv'
    db = pd.read_csv(l)
    coun = db['Country_Region'].unique().tolist()
    return coun
 
#countries = country_list()

#for prototip
countries = ['Afghanistan','Australia', 'Brazil', 'Bulgaria', 'China', 'Cyprus', 'Denmark', 'Egypt', 'Germany', 'Greece', 
             'Hungary', 'India', 'Israel', 'Italy', 'Japan', 'Kazakhstan', 'Kyrgyzstan',  'Latvia', 'Lithuania', 'Maldives', 
             'Moldova', 'Norway', 'Russia', 'Slovenia', 'Spain', 'Sweden', 'Turkey', 'US', 'Ukraine',
             'United Arab Emirates', 'United Kingdom', 'Zimbabwe'  ]
for country in countries:
    print (country)
    count_new_infected(country,parser)
