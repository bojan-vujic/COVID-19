#!/usr/bin/env python
# coding: utf-8

# Covid-19  update file
# Process files for certain dates

import datetime as dt
from datetime import date, timedelta
import pandas as pd

def read_data_from_github(baseURL, date_to_process):

    Confirmed = pd.read_csv(baseURL + date_to_process + "_Confirmed.csv", index_col=0).T
    Death     = pd.read_csv(baseURL + date_to_process + "_Death.csv",     index_col=0).T
    Recovered = pd.read_csv(baseURL + date_to_process + "_Recovered.csv", index_col=0).T

    confirmed = pd.DataFrame(data=Confirmed).T\
                .groupby('Date\Country').sum()\
                .sort_values([date_to_process], ascending=False).T

    recovered = pd.DataFrame(data=Recovered).T\
                .groupby('Date\Country').sum()\
                .sort_values([date_to_process], ascending=False).T

    death     = pd.DataFrame(data=Death).T\
                .groupby('Date\Country').sum()\
                .sort_values([date_to_process], ascending=False).T

    return confirmed, recovered, death

def return_yesterday(day):
    '''day = "03-28-2020"
    '''
    d1 = dt.datetime.strptime(day, '%m-%d-%Y').date()
    d2 = d1 - timedelta(days=1)
    return str(d2.strftime('%m-%d-%Y'))

# Define some variables
baseURL = "https://raw.githubusercontent.com/bojan-vujic/COVID-19/master/Data/"
baseURL = "CSV_data/Github/"
baseURL_local = baseURL

# first_date = "04-01-2020"
# OR

import sys

d = dt.datetime.today()
first_date = d.strftime('%m-%d-%Y')

print(sys.argv)

first_date = str(sys.argv[1])
sec_to_last_date = return_yesterday(first_date)
print("First day = %s\nDay before = %s" % (first_date, sec_to_last_date))



# Read new data
# new data for first_date
data = pd.read_csv("CSV_data/Daily_csv/%s.csv" % first_date, index_col=0)\
        .groupby('Date\Country').sum().sort_values(['Confirmed'], ascending=False).T

# Old data for 1 day before first_date
con, red, dea = read_data_from_github(baseURL, sec_to_last_date)
Confirmed, Recovered, Deaths = con.T, red.T, dea.T

# create a new empty column for "first_day"
Confirmed[first_date] = ""
Recovered[first_date] = ""
Deaths[first_date]    = ""

# Update
c = pd.DataFrame(data=Confirmed).T
r = pd.DataFrame(data=Recovered).T
d = pd.DataFrame(data=Deaths).T

print("New data for date ", first_date)

missing_cols = []

for col in data.columns:
    if col in c.columns:
        new_c, new_d, new_r = data.get(col)
        old_c, old_d, old_r = c.at[sec_to_last_date,col], d.at[sec_to_last_date,col], r.at[sec_to_last_date,col]
        
        # update old_c
        if new_c >= old_c:
            c.xs(first_date)[col] = new_c
        else:
            c.xs(first_date)[col] = old_c
            print("c_old > c_new : %4i %4i %-20s" % (old_c, new_c, col))
        
        # update old_d and old_r
        d.xs(first_date)[col] = new_d
        r.xs(first_date)[col] = new_r
    else:
        pass

# update if missing
for col in c.columns:
    if col not in data.columns:
        c.at[first_date,col] = c.at[sec_to_last_date,col]
        r.at[first_date,col] = r.at[sec_to_last_date,col]
        d.at[first_date,col] = d.at[sec_to_last_date,col]

cc = pd.DataFrame(data=c)
rr = pd.DataFrame(data=r)
dd = pd.DataFrame(data=d)

for col in data.columns:
    if col not in cc.columns:
        print(col)
        cc[col] = [0] * len(c)
        cc.at[first_date,col] = data[col][0]
    if col not in dd.columns:
        #print(col)
        dd[col] = [0] * len(d)
        dd.at[first_date,col] = data[col][1]
    if col not in rr.columns:
        #print(col)
        rr[col] = [0] * len(r)
        rr.at[first_date,col] = data[col][2]

ccc = pd.DataFrame(data=cc).T.sort_values([first_date], ascending=False).T
rrr = pd.DataFrame(data=rr).T.sort_values([first_date], ascending=False).T
ddd = pd.DataFrame(data=dd).T.sort_values([first_date], ascending=False).T

ccc.T.to_csv(baseURL_local + "%s_Confirmed.csv" % first_date)
rrr.T.to_csv(baseURL_local + "%s_Recovered.csv" % first_date)
ddd.T.to_csv(baseURL_local + "%s_Death.csv" % first_date)




