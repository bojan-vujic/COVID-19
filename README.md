# `COVID-19 data and graphs`

<p align="center">
  <img src="https://github.com/bojan-vujic/COVID-19/blob/master/Top_25_prediction/plots/World_lin.jpg" alt="World COVID-19 prediction" width="800">
</p>
<p align="center">
  <img src="https://github.com/bojan-vujic/COVID-19/blob/master/Top_25_prediction/plots/Italy_lin.jpg" alt="Italy COVID-19 prediction" width="800">
</p>
<p align="center">
  <img src="https://github.com/bojan-vujic/COVID-19/blob/master/Top_25_prediction/plots/Sweden_lin.jpg" alt="Sweden COVID-19 prediction" width="800">
</p>

<p align="center">
  <img src="https://github.com/bojan-vujic/COVID-19/blob/master/Top_25_current/plots/World_lin.jpg" alt="World COVID-19 prediction" width="800">
</p>
<p align="center">
  <img src="https://github.com/bojan-vujic/COVID-19/blob/master/Top_25_current/plots/Italy_lin.jpg" alt="Italy COVID-19 prediction" width="800">
</p>
<p align="center">
  <img src="https://github.com/bojan-vujic/COVID-19/blob/master/Top_25_current/plots/Sweden_lin.jpg" alt="Sweden COVID-19 prediction" width="800">
</p>

`Directories:`
=============

* `Country_flags`  : contains flag for each country, named as `${country_iso}.png`,
* `Country_images` : images of maps for each country, named as above,
* `Data/`   : csv files containing COVID-19 data for each day starting from 01-22-2020.
* `Graphs/` : some data plots for each country
* `Scripts` : the main directory to work from. It contains the following:
  - [`1-COVID-19_Process_daily_file_from_Worldometer.ipynb`](https://github.com/bojan-vujic/COVID-19/blob/master/Scripts/1-COVID-19_Process_daily_file_from_Worldometer.ipynb)
  - [`1-COVID-19_Process_daily_file_from_Worldometer.py`](https://github.com/bojan-vujic/COVID-19/blob/master/Scripts/1-COVID-19_Process_daily_file_from_Worldometer.py) Modified so it can take an argument from the command line,
  - [`2-COVID-19_Data_analysis.ipynb`](https://github.com/bojan-vujic/COVID-19/blob/master/Scripts/2-COVID-19_Data_analysis.ipynb) This notebook will make a plot of current data for number of countries,
  - [`3-COVID-19_Model_prediction-with_SUBPLOT.ipynb`](https://github.com/bojan-vujic/COVID-19/blob/master/Scripts/3-COVID-19_Model_prediction-with_SUBPLOT.ipynb) This notebook will make some fancy plots alongside predictions for number of confirmed cases,
  - [`covid-19.sh`](https://github.com/bojan-vujic/COVID-19/blob/master/Scripts/covid-19.sh) This bash script will download current data from [`worldometer`](https://www.worldometers.info/coronavirus/) page and further process. As a result it will save 4 csv files: Confirmed, Recovered, Death, Critical. It will work together with the script [`1-COVID-19_Process_daily_file_from_Worldometer.py`](https://github.com/bojan-vujic/COVID-19/blob/master/Scripts/1-COVID-19_Process_daily_file_from_Worldometer.py).
  - [`functions.py`](https://github.com/bojan-vujic/COVID-19/blob/master/Scripts/functions.py) It contains most of the functions without which notebooks won't work.
  
  
  





`Use`
==========
All the code for data analysis has been written in Python 3, though most parts would work in Python 2 as well (not tested).

If you discover some bugs or even worked out a way to fix them, that would be both exelent.

`Data source`
============
Currently only 1 data source have been used for number of cases:

* https://www.worldometers.info/coronavirus/ - Webpage with updated information abount the virus around the globe.

To download the data for today from Worldometer, run the bash script [`covid-19.sh`.](https://github.com/bojan-vujic/COVID-19/blob/master/Scripts/covid-19.sh)

Sources for country flags:
* https://en.wikipedia.org/wiki/Gallery_of_sovereign_state_flags

Sources for country maps:
* https://github.com/djaiss/mapsicon - they are further processed using a simple bash script (included) by my personal preferences.

```
$ bash covid-19.sh
Downloading https://www.worldometers.info/coronavirus/

Processing the file 04-06-2020.html
Converting html file using html2txt.
Processing countries, 212 in total.

   Progress =   100.00 %

done
Have a nice day :)
```

It will download the file `MM-DD-YYYY.csv` containing informations about number of total confirmed cases, number of recovered and death cases for each country that are currently presented at the [Worldometer page](https://www.worldometers.info/coronavirus/).

`Contact`
=======

Any questions, comments and/or suggestions are more than welcome at: bojan.vujic@mmk.su.se

Have a nice day! :)

