import pandas as pd
import numpy as np
import datetime as dt
from datetime import date, timedelta

import scipy

from scipy.optimize import *
from scipy.interpolate import interp1d


# Some styles
# tables are large, use set_option if you want to display whole table
pd.set_option('display.max_rows', 200)
    
heading_properties = [('font-size', '16px')]
cell_properties    = [('font-size', '16px')]

dfstyle = [{'selector':'','props':[('border','5px solid #7a7')]},\
            dict(selector="th", props=heading_properties),\
            dict(selector="td", props=cell_properties)]




def read_data_from_github(baseURL, date_to_process):
    '''This function will read the data from github page,
    given the baseURL and date_to_process.'''
    
    Confirmed = pd.read_csv(baseURL + date_to_process + "_Confirmed.csv", index_col=0).T  # .T will transpose the table
    Death     = pd.read_csv(baseURL + date_to_process + "_Death.csv",     index_col=0).T
    Recovered = pd.read_csv(baseURL + date_to_process + "_Recovered.csv", index_col=0).T

    # 1. if there are duplicate countries, handle them in the following way
    # 2. most probably I already sorted the data, but just in case...
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


def display_data(TOP_n_countries, Last_n_days, pd_dataframe):
    '''Display cases for TOP_n_countries and Newest_n_days'''
    return pd_dataframe.tail(Last_n_days).T.head(TOP_n_countries).style.set_table_styles(dfstyle)

def display_data_for_selected_countries(countries_to_display, Last_n_days, date_to_process, pd_dataframe):
    table = pd.DataFrame(data=pd_dataframe[countries_to_display]).T.sort_values([date_to_process], ascending=False).T.tail(Last_n_days)
    return table.T.style.set_table_styles(dfstyle)

def world_population():
    '''It will read a table from github. The url is already defined.'''
    return pd.read_csv("https://raw.githubusercontent.com/bojan-vujic/COVID-19/master/World_population.csv",index_col=0).T

def display_population(pd_dataframe):
    return pd_dataframe.style.set_table_styles(dfstyle)

def get_population_area_and_country_ISO_code(country, population_df):
    '''For the given country it will return: population, area and country ISO code.
    e.g. country = "Sweden", population_df = population
    '''
    population = int(population_df[country].to_numpy()[0])
    area       = int(population_df[country].to_numpy()[1])
    iso_code   = str(population_df[country].to_numpy()[2])
    return population, area, iso_code

def data_gt_or_eq_than_min_cases(country, min_cases, confirmed, recovered, death):
    '''This functions will find the data for cases larger than min_cases
    and will return several arrays: time(days), number of cases for the given country, ...'''
    
    dates = []
    table = pd.DataFrame(data=confirmed[country])
    for index, rows in table.iterrows():
        x = str(index)
        dates.append(x)
    x_time1 = [dt.datetime.strptime(d,'%m-%d-%Y').date() for d in dates]
    
    conf_cases1  = confirmed[country].to_numpy()
    recov_cases1 = recovered[country].to_numpy()
    death_cases1 = death[country].to_numpy()
    
    x_time2, conf_cases2, recov_cases2, death_cases2, active_cases = [], [], [], [], []
    
    for el in range(len(conf_cases1)):
        if conf_cases1[el] >= min_cases:
            x_time2     .append(x_time1[el])
            conf_cases2 .append(conf_cases1[el])
            recov_cases2.append(recov_cases1[el])
            death_cases2.append(death_cases1[el])
            delta = conf_cases1[el] - recov_cases1[el] - death_cases1[el]
            active_cases.append(delta)
    
    x_day  = np.arange(1, 1+len(x_time2))
    
    return x_time2, x_day, conf_cases2, recov_cases2, death_cases2, active_cases

# Similar to the previous function, returns active cases
def return_active_cases(country, min_cases, df_c, df_r, df_d):
    '''This functions will return an array with number of active cases.'''
    conf_cases = []
    table = pd.DataFrame(data=df_c[country])
    for index, rows in table.iterrows():
        y = int(rows[0])
        if y >= min_cases:
            conf_cases.append(y)

    last_n = len(conf_cases)

    dea_array = df_d[country].to_numpy()[len(df_d[country])-last_n:]
    rec_array = df_r[country].to_numpy()[len(df_r[country])-last_n:]
    
    active_cases = []
    for el in range(last_n):
        num = conf_cases[el] - dea_array[el] - rec_array[el]
        active_cases.append(num)
    return active_cases


def list_of_countries(pd_dataframe):
    '''This function will return list of countries within given pd_dataframe.'''
    return [str(country) for country in pd_dataframe.columns]


def return_time_interval(Last_n_days, n_x_ticks,total_points):
    time_interval = 1
    if Last_n_days <= total_points:
        time_interval = int(np.round(Last_n_days/n_x_ticks, 0)) if n_x_ticks <= Last_n_days else 1 
    else:
        time_interval = int(np.round(total_points/n_x_ticks, 0)) if n_x_ticks <= total_points else 1 
    return time_interval

def return_time_interval_model(n_x_ticks, array):
    time_interval = 1
    length = len(array)
    if n_x_ticks <= length:
        time_interval = int(np.round(length/n_x_ticks, 0)) if n_x_ticks <= Last_n_days else 1 
    else:
        time_interval = int(np.round(len(confirmed)/n_x_ticks, 0)) if n_x_ticks <= len(confirmed) else 1 
    return time_interval


def logistic_function(x, a, b, c, d):
    y = a/(1 + np.exp(-b*(x-c))) + d
    return y


def optimal_parameters(i, country, confirmed, recovered, death):
    RMSs, parameter_array = [], []
    MINs = range(0, 1001, 5)

    # Though this method is relatively fast enough, there is still a more efficient way of doing this.
    # Try Scipy optimiziation of objective function
    for min_cases in MINs:
        x_time, x_day, conf_cases = data_gt_or_eq_than_min_cases(country, min_cases, confirmed, recovered, death)[:3]

        if len(conf_cases) >= 4:
            params, pcov = curve_fit(logistic_function, x_day, conf_cases, \
                                     maxfev=1000000, method = 'lm', absolute_sigma=False)
            yfit = logistic_function(x_day, *params)
            rms = np.round(np.sqrt(np.sum((conf_cases - yfit)**2)), 3)
            RMSs.append(rms)
            parameter_array.append(params)
        else:
            RMSs.append(10**10) # arbitrarily large number
            parameter_array.append([0, 0, 0, 0])
    counter = 0
    opt_min = 0
    opt_params = []
    for jj in range(len(RMSs)):
        if RMSs[jj] == np.min(RMSs):
            counter += 1
            if counter == 1:
                #print("%2i %-25s %4i  %8.1f | %3i" % (i+1, country, len(conf_cases), RMSs[jj], MINs[jj]))
                opt_min = MINs[jj]
                opt_params = parameter_array[jj]
    return opt_params, int(opt_min)


def logistic_curve(x_time, x_day, predict_for_n_days, a, b, c, d):
    logistic_y = [logistic_function(x, a, b, c, d) for x in x_day]
    logistic_x = [x for x in x_time]
    first_day = x_time[len(x_time) - 1]

    lg_x, lg_y = [], []
    for el in range(0, predict_for_n_days + 1):
        day = first_day + timedelta(days=el)
        lg_y.append(logistic_function((el + np.max(x_day)), a, b, c, d))
        logistic_y.append(logistic_function((el + np.max(x_day)), a, b, c, d))
        lg_x.append(day)
        logistic_x.append(day)

    return logistic_x, logistic_y, lg_x, lg_y

