from __future__ import division
import pandas as pd
import numpy as np
import datetime as dt
from datetime import date, timedelta

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from PIL import Image
import requests

import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
    
from matplotlib import rc
rc('text', usetex=True)
rc('font', family='serif')

import matplotlib.gridspec as gridspec
import matplotlib.offsetbox as offsetbox
custom_preamble = {
    "text.usetex": True,
    "text.latex.preamble": [
        r"\usepackage{amsmath}", # for the align enivironment
        ],
    }
plt.rcParams.update(custom_preamble)

from matplotlib import pylab
from pylab import *


def get_data_for_last_n_days(country, Last_n_days, pd_dataframe):
    '''This functions will find the data for Last_n_days
    and will return two main arrays: time(days) and number of cases for the given country'''
    dates, y_cases = [], []
    table = pd.DataFrame(data=pd_dataframe[country])
    for index, rows in table.iterrows():
        x = str(index)
        y = int(rows[0])
        dates.append(x)
        y_cases.append(y)
    x_time = [dt.datetime.strptime(d,'%m-%d-%Y').date() for d in dates]
    x_day = np.arange(1, len(y_cases)+1, 1)
    return x_time[-Last_n_days:], x_day[:Last_n_days], y_cases[-Last_n_days:]


def thousand_separator(number):
    '''Return number 5364 into 5 364, hence .replace(",", " ")'''
    return f"{number:,}".replace(",", " ")

# We are interested into the most recent data, so safely use day = date_to_process
def conf_rec_dea(country, day, confirmed, recovered, death):
    '''This function will return number of each cases
    for given country/date.
    example: conf_rec_dea('Sweden', 'MM-DD-YYYY')
    '''
    x1 = confirmed.at[day, country]
    x2 = recovered.at[day, country]
    x3 = death    .at[day, country]
    return x1, x2, x3

def since_one_day_before(country, date_to_process, confirmed, recovered, death):
    '''returns an array with difference in
    confirmed, recovered, death
    '''
    array_one        = conf_rec_dea(country, date_to_process, confirmed, recovered, death)
    array_day_before = conf_rec_dea(country, return_yesterday(date_to_process), confirmed, recovered, death)
    since_yesterday = np.subtract(array_one, array_day_before)
    return since_yesterday[0], since_yesterday[1], since_yesterday[2] # with the reason, instead of since_yesterday

def country_image_url(country_iso_code):
    # import country image
    image_url = "https://raw.githubusercontent.com/bojan-vujic/COVID-19/master/Country_images/"
    image_url = str(image_url + country_iso_code + '.png')
    return image_url

def country_flag_url(country_iso_code):
    image_url = "https://raw.githubusercontent.com/bojan-vujic/COVID-19/master/Country_flags/"
    image_url = str(image_url + country_iso_code + '.png')
    return image_url


# The following function will get the data for the given country (confirmed, recovered, death)
def get_data(pd_dataframe, country, TOP_n_days):
    '''This functions uses pd dataframe and returns
    an array with the data for TOP_n_days and a given country.'''
    y = []
    array = pd_dataframe[country].to_numpy()
    for el in range(len(array)):
        y.append(array[el])
    return y[-TOP_n_days:]


def return_yesterday(day):
    '''day = "03-28-2020"
    '''
    d1 = dt.datetime.strptime(day, '%m-%d-%Y').date()
    d2 = d1 - timedelta(days=1)
    return str(d2.strftime('%m-%d-%Y'))


def make_plot(i, country, x_time, y_confirmed, y_recovered, y_death, active_cases, SCALE, country_population,\
            x_confirmed, x_recovered, x_death, Last_n_days, delta_conf, delta_rec, delta_dea,\
            image_url, countries_to_display, fig_name, time_interval):

    plot_background = (1.0, 0.9803921568627451, 0.9803921568627451, 0.3)
    page_background = (219/255, 223/255, 239/255, 0.1)
    
    y_size = 8
    x_size = 1.55 * y_size
    x_size = 1.25 * y_size
    
    fig = plt.figure(figsize=(x_size, y_size))
    
    fig.patch.set_facecolor(page_background)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = time_interval))
        
    lw = 4
    ms = 9
    # plot confirmed data
    plt.plot(x_time, y_confirmed, marker='o',markeredgecolor='black', markerfacecolor='yellow', color="royalblue",
                     linestyle='-',  lw=lw, ms=ms, label=r'Confirmed', zorder=200,markeredgewidth=1.5, alpha=0.95)
    
    # plot recovered data
    plt.plot(x_time, y_recovered, marker='o',markeredgecolor='black', markerfacecolor='yellow', color="limegreen",
                     linestyle='-',  lw=lw, ms=ms, label=r'Recovered', zorder=200,markeredgewidth=1.5, alpha=0.95)
    
    # plot death data
    plt.plot(x_time, y_death, marker='o',markeredgecolor='black', markerfacecolor='yellow', color="red",
                     linestyle='-',  lw=lw, ms=ms, label=r'Death', zorder=200,markeredgewidth=1.5, alpha=0.95)
    
    # plot active cases
    plt.plot(x_time, active_cases, marker='h',markeredgecolor='black', markerfacecolor='yellow', color="purple",
                     linestyle='-',  lw=lw, ms=ms, label=r'Active cases', zorder=200,markeredgewidth=1.5, alpha=0.95)
    
    plt.fill_between(x_time, y_confirmed,y_recovered,color='khaki',alpha=.1)
    plt.fill_between(x_time ,y_recovered,y_death, color='limegreen',alpha=.02)
    plt.fill_between(x_time, y_death,color='red',alpha=.07)
    
    country_image_position = [0.88, 0.332, 0.34, 0.34]  # [left, bottom, width, height])
    
    plt.ylabel(r'Number of cases', size=20)
    pylab.yticks(fontsize=16)
    pylab.xticks(fontsize=16)
    
    if SCALE == "log":
        pyplot.yscale('log')
    
    y_lim_bottom = 0 if SCALE == 'lin' else 1
    pylab.ylim(bottom = y_lim_bottom)
    pylab.xlim(left = x_time[0], right = x_time[len(x_time) - 1])
    
    grid(b=True, which='major' , linestyle='-', color= 'lightgrey', linewidth=0.8)
    grid(b=True, which='minor', linestyle='--', color= 'lightgrey', linewidth=0.7)
    
    ax1 = fig.add_subplot(111)
    for axis in ['top','bottom','left','right']:
        ax1.spines[axis].set_linewidth(1.2)
        ax1.tick_params(which='major',axis='both', color='black', bottom=1, top=1, left=1, right=1,
               length=8, width=1.0, zorder=2000, direction = "in")
        ax1.tick_params(which='minor',axis='both', color='black', bottom=1, top=1, left=1, right=1,
               length=4, width=1.0, zorder=2000, direction = "in")
    plt.legend(loc = 2, ncol=1, fancybox=True, numpoints=1, markerscale=0.8,
                fontsize=16, framealpha=0.7).set_zorder(300)
    ax1.set_facecolor(plot_background)
    plt.gcf().autofmt_xdate()
    
    mil_population = country_population / 1000000
    # Text lines (this can be also done with "join" in an more elegant way)
    t1 = r'\begin{tabular}{lcr} '
    t2 = r'Population M &=& %5.2f' % (mil_population) + '\\\\'
    t3 = r'Confirmed/1M &=& %5.2f' % (x_confirmed/mil_population) + '\\\\'
    t4 = r'Confirmed &=& %5s' % str(x_confirmed) + '\\\\'
    t5 = r'Recovered &=& %5s' % str(x_recovered) + '\\\\'
    t6 = r'Death &=& %5s' % str(x_death)
    t7 = r'\end{tabular}'
    text = t1 + t2 + t3 + t4 + t5 + t6 + t7
    
    props  = dict(boxstyle='round', facecolor='snow', alpha=0.5, edgecolor='gray', pad = 0.6, zorder = 2000)
    a, aa = 0.925, 0.16
    fig.text(a, 0.3, text, fontsize=17, verticalalignment='top', horizontalalignment='left', bbox=props)
    fig.text(0.12, 0.9, 'Plot for %i days' % Last_n_days, fontsize=18, horizontalalignment = 'left')
    fig.text(a, 0.9, 'Change within 24h', fontsize=18)
    fig.text(0.5, 0.9, r'%i. %s' % (i+1, country), fontsize=24, horizontalalignment='center', fontweight='bold')
    #fig.text(0.1, 0.9, r'%i' % (i + 1), fontsize=20, horizontalalignment='center')
    
    # change since yesterday
    # right hand side of the plot
    cpad = 0.4
    props  = dict(boxstyle='round', facecolor='crimson', alpha=0.3, edgecolor='gray', pad=cpad, zorder = 2000)
    fig.text(a, 0.845, r' Confirmed ', fontsize=18, horizontalalignment='left', bbox=props)
    props  = dict(boxstyle='round', facecolor='crimson', alpha=0.15, edgecolor='gray', pad=cpad, zorder = 2000)
    fig.text(a + aa, 0.845, r'%+6d' % delta_conf, fontsize=18, horizontalalignment='left', bbox=props)
    
    props  = dict(boxstyle='round', facecolor='lime', alpha=0.3, edgecolor='gray', pad=cpad, zorder = 2000)
    fig.text(a, 0.775, r' Recovered ', fontsize=18, horizontalalignment='left', bbox=props)
    props  = dict(boxstyle='round', facecolor='lime', alpha=0.15, edgecolor='gray', pad=cpad, zorder = 2000)
    fig.text(a + aa, 0.775, r'%+6d' % delta_rec, fontsize=18, horizontalalignment='left', bbox=props)
    
    props  = dict(boxstyle='round', facecolor='red', alpha=0.3, edgecolor='gray', pad=cpad, zorder = 2000)
    fig.text(a, 0.705, r" Death     ", fontsize=18, horizontalalignment='left', bbox=props)
    props  = dict(boxstyle='round', facecolor='red', alpha=0.15, edgecolor='gray', pad=cpad, zorder = 2000)
    fig.text(a + aa, 0.705, r'%+6d' % delta_dea, fontsize=18, horizontalalignment='left', bbox=props)
    
    # Image of the country
    img = Image.open(requests.get(image_url, stream=True).raw)
    
    ax3 = plt.axes(country_image_position, frameon=True)
    ax3.imshow(img)
    ax3.axis('off')
    
    ppad = 7
    ppadinches = ppad/25.4
    pylab.savefig(fig_name, format='pdf', bbox_inches='tight', \
                  pad_inches = ppadinches,facecolor=page_background)
    for cc in countries_to_display:
        if country == str(cc):
            plt.show()
    plt.close(fig)
    
    return ;














