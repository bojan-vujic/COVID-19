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
    img_url = "https://raw.githubusercontent.com/bojan-vujic/COVID-19/master/Country_images/"
    img_url = str(img_url + country_iso_code + '.png')
    #print("Map url:", img_url)
    return img_url


def country_flag_url(country_iso_code):
    img_url = "https://raw.githubusercontent.com/bojan-vujic/COVID-19/master/Country_flags/"
    img_url = str(img_url + country_iso_code + '.png')
    #print("Flag url:", img_url)
    return img_url


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


def date_after_n_days(first_day, n, fmt):
    '''Fixed format for input first_day = "03-29-2020"
    fmt = %m-%d-%Y, or any other, will format the output.
    If n = -1 and first_day = today, it will return yesterday.
    If n = 0, it will return today with format as fmt.
    If n = 1, it will return tomorrow.
    '''
    d1 = dt.datetime.strptime(first_day, '%m-%d-%Y').date()
    d2 = d1 + timedelta(days=n)
    d2 = d2.strftime(fmt)
    return d2



def make_plot(i, country, x_time, y_confirmed, y_recovered, y_death, active_cases, SCALE, country_population,\
            x_confirmed, x_recovered, x_death, Last_n_days, delta_conf, delta_rec, delta_dea,\
            image_url, flag_url, countries_to_display, fig_name, x_axis_fmt, time_interval, output_format, output_dpi):
    
    plot_background = (1.0, 0.9804, 0.9804, 0.3)
    page_background = (219/255, 223/255, 239/255, 0.1)
    
    y_size = 8
    x_size = 1.55 * y_size
    x_size = 1.25 * y_size
    
    fig = plt.figure(figsize=(x_size, y_size))
    
    fig.patch.set_facecolor(page_background)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(x_axis_fmt))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = time_interval))
    
    lw = 4
    ms = 9
    
    if np.max(y_confirmed) >= 10**3 and np.max(y_confirmed) < 10**6:
        main_string = r'$\times 10^3$'
        scale_factor = 10**3
    elif np.max(y_confirmed) >= 10**6:
        main_string = r'$\times 10^6$'
        scale_factor = 10**6
    else:
        main_string = ''
        scale_factor = 1
    
    y_confirmed  = np.divide(y_confirmed, scale_factor)
    y_recovered  = np.divide(y_recovered, scale_factor)
    y_death      = np.divide(y_death, scale_factor)
    active_cases = np.divide(active_cases, scale_factor)
    
    # plot confirmed data
    plt.plot(x_time, y_confirmed, marker='o',markeredgecolor='black', markerfacecolor='yellow', color="royalblue",
                     linestyle='-',  lw=lw, ms=ms, label=r'Confirmed', zorder=400,markeredgewidth=1.5, alpha=0.95)
    
    # plot active cases
    plt.plot(x_time, active_cases, marker='h',markeredgecolor='black', markerfacecolor='yellow', color="purple",
                     linestyle='-',  lw=lw, ms=ms, label=r'Active cases', zorder=390,markeredgewidth=1.5, alpha=0.95)
    
    # plot recovered data
    plt.plot(x_time, y_recovered, marker='o',markeredgecolor='black', markerfacecolor='yellow', color="limegreen",
                     linestyle='-',  lw=lw, ms=ms, label=r'Recovered', zorder=380,markeredgewidth=1.5, alpha=0.95)
    
    # plot death data
    plt.plot(x_time, y_death, marker='o',markeredgecolor='black', markerfacecolor='yellow', color="red",
                     linestyle='-',  lw=lw, ms=ms, label=r'Death', zorder=370,markeredgewidth=1.5, alpha=0.95)
    
    
    plt.fill_between(x_time, y_confirmed,y_recovered,color='khaki',alpha=.1)
    plt.fill_between(x_time ,y_recovered,y_death, color='limegreen',alpha=.02)
    plt.fill_between(x_time, y_death,color='red',alpha=.07)
    
    country_image_position = [0.88, 0.332, 0.34, 0.34]  # [left, bottom, width, height])
    
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
    
    y_bottom, y_top = ax1.get_ylim()
    locs, labels = yticks()
    
    if np.max(y_confirmed)*scale_factor >= 10**6:
        ax1.yaxis.set_major_locator(MaxNLocator(integer=False))
        ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    else:
        ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    
    y_ticks = [y for y in locs]
    y_ticks = np.array(y_ticks)
    y_ticks = y_ticks[np.logical_and(y_ticks >= y_bottom, y_ticks <= y_top)]
    if np.max(y_confirmed)*scale_factor >= 10**6:
        max_y = len(str(np.max(np.round(y_ticks, 2)))) - 0.32
    else:
        max_y = len(str(int(np.max(y_ticks))))
    
    lpad = (4 - max_y)*7.7 + 10
    
    pylab.ylabel(r'Number of cases %s' % main_string, size=20, labelpad=lpad)
    pylab.yticks(y_ticks, fontsize=16)
    pylab.xticks(fontsize=16)
    
    mil_population = country_population / 10**6
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
    if Last_n_days <= len(y_confirmed):
        fig.text(0.12, 0.9, 'Plot for %i days' % Last_n_days, fontsize=18, horizontalalignment = 'left')
    else:
        fig.text(0.12, 0.9, 'Plot for %i days' % (len(y_confirmed)), fontsize=18, horizontalalignment = 'left')
    fig.text(a, 0.9, 'Change within 24h', fontsize=18)
    fig.text(0.5, 0.9, r'%i. %s' % (i+1, country), fontsize=24, horizontalalignment='center', fontweight='bold')
    
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
    
    # Image of the country flag
    country_flag_position = [0.796, 0.885, 0.12, 0.08]   # top right on the plot
    img = Image.open(requests.get(flag_url, stream=True).raw)
    ax4 = plt.axes(country_flag_position, frameon=True)
    ax4.imshow(img)
    ax4.axis('off')
    
    ppad = 7
    ppadinches = ppad/25.4
    
    if output_format == 'pdf':
        pylab.savefig(fig_name, format=output_format, bbox_inches='tight',
                      pad_inches = ppadinches,facecolor=page_background, zorder = 1)
    
    if output_format == 'jpg' or output_format == 'png':
        pylab.savefig(fig_name, format=output_format, bbox_inches='tight',dpi = output_dpi,
                      pad_inches = ppadinches,facecolor=page_background, zorder = 1)
    
    for cc in countries_to_display:
        if country == str(cc):
            plt.show()
    plt.close(fig)
    
    return ;


def make_model_plot(i, country, x_time, conf_cases, recov_cases, death_cases, active_cases, predictions_enabled, \
                    SCALE, country_population, x_confirmed, x_recovered, x_death, critical, Last_n_days, \
                    delta_conf, image_url, countries_to_display, fig_name, time_interval,\
                    logistic_x, logistic_y, predict_for_n_days, fmt, lg_x, lg_y, flag_url, date_to_process, \
                    time_array, time_interval_rate, conf_cases_rate, death_cases_rate,\
                    Last_n_days_for_rate, x_axis_fmt, output_format, output_dpi):
    
    plot_background = (1.0, 0.9803921568627451, 0.9803921568627451, 0.3)
    page_background = (219/255, 223/255, 239/255, 0.1)
    
    y_size = 8
    x_size = 1.55 * y_size
    x_size = 1.25 * y_size
    
    fig = plt.figure(figsize=(x_size, y_size))
    fig.patch.set_facecolor(page_background)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(x_axis_fmt))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = time_interval))
    
    lw = 4
    ms = 9
    if np.max(logistic_y) >= 10**3 and np.max(logistic_y) < 10**6:
        main_string = r'$\times 10^3$'
        scale_factor = 10**3
    elif np.max(logistic_y) >= 10**6:
        main_string = r'$\times 10^6$'
        scale_factor = 10**6
    else:
        main_string = ''
        scale_factor = 1

    conf_cases   = np.divide(conf_cases, scale_factor)
    logistic_y   = np.divide(logistic_y, scale_factor)
    lg_y         = np.divide(lg_y, scale_factor)
    recov_cases  = np.divide(recov_cases, scale_factor)
    death_cases  = np.divide(death_cases, scale_factor)
    active_cases = np.divide(active_cases, scale_factor)
    
    if predictions_enabled == 'Yes':
        plt.plot(x_time, conf_cases, marker='o',markeredgecolor='black', markerfacecolor='yellow',
             color="royalblue", linestyle='',  lw=lw, ms=ms, label=r'Confirmed', zorder=300,markeredgewidth=1.5, alpha=0.8)
        # plot logistic curve
        plt.plot(logistic_x, logistic_y, marker='', color="royalblue", linestyle='-',
                 lw=lw, label=r'Predicted', zorder=200, alpha=0.95)
        
        plt.plot(lg_x[1:], lg_y[1:], marker='o',markeredgecolor='black', markerfacecolor='snow', color="royalblue",
                     linestyle='-',  lw=lw, ms=ms, zorder=220,markeredgewidth=1.5, alpha=0.9)
        
        plt.fill_between(lg_x, lg_y, color='royalblue',alpha=.1, hatch="X", lw=2, zorder = 500)
        
        # for some styling at the top right corner of the plot
        x1, y1 = x_time[len(x_time) - 1], conf_cases[len(conf_cases) - 1]
        x2, y2 = lg_x[len(lg_x) - 1], lg_y[len(lg_y) - 1]
        delta  = int(np.round((y2 - y1)*scale_factor, 0))
        
    else:
        plt.plot(x_time, conf_cases, marker='o',markeredgecolor='black', markerfacecolor='yellow',
             color="royalblue", linestyle='-', lw=lw, ms=ms, label=r'Confirmed', zorder=300,markeredgewidth=1.5, alpha=0.95)
    
    plt.plot(x_time, active_cases, marker='',color="maroon", linestyle='-',lw=2.5, label=r'Active', zorder=10,alpha=0.6)
    plt.plot(x_time, recov_cases, marker='',color="limegreen", linestyle='-',lw=2.5, label=r'Recovered', zorder=10,alpha=0.6)
    
    
    plt.fill_between(x_time, conf_cases, recov_cases, color='khaki',alpha=.1)
    plt.fill_between(x_time, recov_cases, death_cases, color='limegreen',alpha=.02)
    plt.fill_between(x_time, death_cases, color='red',alpha=.07)
    
    if SCALE == "log":
        pyplot.yscale('log')
    
    y_lim_bottom = 0 if SCALE == 'lin' else 1
    pylab.ylim(bottom = y_lim_bottom)
    if predictions_enabled == 'Yes':
        pylab.xlim(left = x_time[0] - timedelta(days=0), right = lg_x[len(lg_x)-1])
    else:
        pylab.xlim(left = x_time[0] - timedelta(days=0), right = x_time[len(x_time)-1])
    
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
    
    # Set the padding on y axis label
    # For 1 plot you don't have to worry. When have multipage pdf with several plots,
    # it can happen that axis is shifting a lot, left and right when switching pages. This is due to
    # different number of diggits on y-axis labels on different plots.
    # Personally, I don't like it, so this will do the trick.
    # If you have more elegant way of doing it, please share. :)
    # -------------------------------------
    if np.max(logistic_y)*scale_factor >= 10**6:
        ax1.yaxis.set_major_locator(MaxNLocator(integer=False))
        ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    else:
        ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    y_bottom, y_top = ax1.get_ylim()
    locs, labels = yticks()
    
    y_ticks = [y for y in locs]
    y_ticks = np.array(y_ticks)
    y_ticks = y_ticks[np.logical_and(y_ticks >= y_bottom, y_ticks <= y_top)]
    if np.max(logistic_y)*scale_factor >= 10**6:
        lens = [len(str(np.round(y, 2))) for y in y_ticks]
        max_y = np.max(lens) - 0.35
    else:
        max_y = len(str(int(np.max(y_ticks))))
    
    lpad = (4 - max_y)*7.7 + 10
    pylab.ylabel(r'Number of cases %s' % main_string, size=20, labelpad=lpad)
    pylab.yticks(y_ticks, fontsize=16)
    pylab.xticks(fontsize=16)
    
    # Text lines (this can be also done with "join" in an more elegant way)
    #-------------------------------------------------------------------------
    t0 = r'Total on %s \\ \\' % (date_after_n_days(date_to_process, 0, fmt))
    t1 = r'\begin{tabular}{lclcr} '
    t2 = r'Confirmed & &:& & %5s' % str(thousand_separator(x_confirmed)) + '\\\\'
    t3 = r'Recovered & &:& & %5s' % str(thousand_separator(x_recovered)) + '\\\\'
    t4 = r'Death     & &:& & %5s' % str(thousand_separator(x_death)) + '\\\\'
    t5 = r'Critical  & &:& & %5s' % str(thousand_separator(critical))
    t6 = r'\end{tabular}'
    text1 = t0 + t1 + t2 + t3 + t4 + t5 + t6
    
    fig.text(0.5, 0.9, r'%i. %s' % (i+1, country), fontsize=24, horizontalalignment='center', fontweight='bold')
    props  = dict(boxstyle='round', facecolor='snow', alpha=0.5, edgecolor='gray', pad = 0.6, zorder = 2000)
    
    #-----------------------------------------------------------------------
    if predictions_enabled == 'Yes':
        
        def predict(lg_y, num, scale_factor, x_confirmed):
            try:
                predicted = int(np.round(lg_y[num] * scale_factor))
                since_today = int(np.round((predicted - x_confirmed), 0))
                a = f"+{since_today:,}".replace(",", " ")
                b = f"{predicted:,}".replace(",", " ")
                return a, b 
            except:
                return 'NAN'
        
        def get_line(day, a, b):
            return r'%s & %5s & %5s' % (day, a, b)
        
        sc = scale_factor
        
        # Text lines (this can be also done with "join")
        #-------------------------------------------------------------------------
        td = x_confirmed
        dtp = date_to_process
        pnd = predict_for_n_days
        
        t_n0    = r'\begin{tabular}{c} '
        t_n1    = r'Predictions on %s \\' % (date_after_n_days(dtp, 0, fmt))
        t_n2  = r'\end{tabular}\\'
        tn_nol = t_n0 + t_n1 + t_n2
        t_first = r'\begin{tabular}{lrr} '
        t_last  = r'\end{tabular}'
        
        if pnd > 0:
            fig.text(0.12, 0.9, 'Plot for %i + %i days' % (Last_n_days, predict_for_n_days), \
                     fontsize=18, horizontalalignment = 'left')
            fig.text(0.87, 0.315, text1, fontsize=15, verticalalignment='center', horizontalalignment='right', bbox=props)
            
            t1 = get_line(date_after_n_days(dtp, 1, fmt), *predict(lg_y, 1, sc, td))
            
            if pnd == 1:
                text2 = tn_nol + t_first + t1 + t_last
            else:
                t2 = get_line(date_after_n_days(dtp, 2, fmt), *predict(lg_y, 2, sc, td))
                text0 = tn_nol + t_first + t1 + '\\\\' + t2
                
                if pnd == 2:
                    text2 = text0 + t_last
                
                if pnd == 3:
                    t3 = get_line(date_after_n_days(dtp, 3, fmt), *predict(lg_y, 3, sc, td))
                    text2 = text0 + '\\\\' + t3 + t_last
                
                if pnd > 3:
                    t3 = get_line(date_after_n_days(dtp, 3, fmt), *predict(lg_y, 3, sc, td))
                    t4 = get_line(date_after_n_days(dtp, pnd, fmt), *predict(lg_y, pnd, sc, td))
                    text2 = text0 + '\\\\' + t3 + '\\\\' + t4 + t_last
                    
            fig.text(1.103, 0.86, text2, fontsize=16, verticalalignment='center', horizontalalignment='center', bbox=props)
        else:
            fig.text(0.12, 0.9, 'Plot for %i days' % Last_n_days, fontsize=18, horizontalalignment = 'left')
            fig.text(1.105, 0.86, text1, fontsize=15, verticalalignment='center', horizontalalignment='center', bbox=props)
    else:
        fig.text(0.12, 0.9, 'Plot for %i days' % Last_n_days, fontsize=18, horizontalalignment = 'left')
        fig.text(1.105, 0.86, text1, fontsize=15, verticalalignment='center', horizontalalignment='center', bbox=props)
    
    fig.text(0.95, 0.725, 'Daily cases in the last %i days' % Last_n_days_for_rate, fontsize=18, ha='left')
    
    # Image of the country flag
    country_flag_position = [0.796, 0.885, 0.12, 0.08]   # top right on the plot
    img = Image.open(requests.get(flag_url, stream=True).raw)
    ax4 = plt.axes(country_flag_position, frameon=True)
    ax4.imshow(img)
    ax4.axis('off')
    
    # this can be implemented within function arguments.
    arrays_to_plot     = [conf_cases_rate,        death_cases_rate]
    bar_plot_colors    = ['royalblue',            'red']
    legend_labels      = ['Daily conf.',          'Daily deaths']
    bar_plot_positions = [[0.955, 0.2, 0.3, 0.25], [0.955, 0.465, 0.3, 0.25]]
    
    # make bar plots
    #----------------------------------------------------------------------------------------------------
    for idx in [0, 1]:
        array_to_plot = arrays_to_plot[idx]
        if np.max(array_to_plot) >= 10**4:
            legend_label = r'%s $\times 10^3$' % legend_labels[idx]
            y_array = np.divide(array_to_plot, 10**3)
        else:
            legend_label = r'%s' % legend_labels[idx]
            y_array = np.divide(array_to_plot, 1)
        
        bar_plot_position = bar_plot_positions[idx]
        ax5 = plt.axes(bar_plot_position)
        ax5.bar(time_array, y_array, width = 0.7, alpha=0.7, color=bar_plot_colors[idx], zorder=500, label=legend_label)
        ax5.set_facecolor(plot_background)
        grid(b=True, which='major' , linestyle='-', color= 'lightgrey', linewidth=0.8)
        grid(b=True, which='minor', linestyle='--', color= 'lightgrey', linewidth=0.7)
        ax5.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.ylim(bottom = 0)
        plt.xlim(left = time_array[0] - timedelta(days=1), right = time_array[len(time_array)-1] + timedelta(days=1))
        plt.yticks(fontsize=13)
        if idx == 0:
            plt.xticks(fontsize=13, rotation=30, ha='right')
        else:
            plt.xticks(visible=False)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(x_axis_fmt))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = time_interval_rate))

        for axis in ['top','bottom','left','right']:
            ax1.spines[axis].set_linewidth(1.2)
            ax1.tick_params(which='major',axis='both', color='black', bottom=1, top=1, left=1, right=1,
                   length=8, width=1.0, zorder=2000, direction = "in")
            ax1.tick_params(which='minor',axis='both', color='black', bottom=1, top=1, left=1, right=1,
                   length=4, width=1.0, zorder=2000, direction = "in")
        ax5.legend(loc = 2, ncol=1, fancybox=True, numpoints=1, markerscale=0.1, fontsize=14, framealpha=0.7).set_zorder(3000)
    #----------------------------------------------------------------------------------------------------
    
    ppad = 7
    ppadinches = ppad/25.4
    
    if output_format == 'pdf':
        pylab.savefig(fig_name, format=output_format, bbox_inches='tight',
                      pad_inches = ppadinches,facecolor=page_background, zorder = 1)
    
    if output_format == 'jpg' or output_format == 'png':
        pylab.savefig(fig_name, format=output_format, bbox_inches='tight',dpi = output_dpi,
                      pad_inches = ppadinches,facecolor=page_background, zorder = 1)
    
    if country in countries_to_display:
        plt.show()
    plt.close(fig)
    
    return ;











