# `COVID-19 data and graphs`

Directories:

* #### Country_flags  : 
* #### Data/   : csv files containing COVID-19 data for each day starting from 01-22-2020.
* #### Graphs/ : some data plots for each country





`Use`
==========
All the code for data analysis has been written in Python 3, though most parts would work in Python 2 as well (not tested).

If you discover some bugs or even worked out a way to fix them, that would be both exelent.

`Data source`
============
Currently only 1 data source have been used for number of cases:

* https://www.worldometers.info/coronavirus/ - Webpage with updated information abount the virus around the globe.

To download the data for today from Worldometer, run the bash script under directory `Bash.`

Sources for country flags:
* https://en.wikipedia.org/wiki/Gallery_of_sovereign_state_flags

Sources for country maps:
* https://github.com/djaiss/mapsicon - they are further processed using a simple bash script (included) by my personal preferences.

```
$ bash covid-19.sh
Downloading https://www.worldometers.info/coronavirus/

Processing the file 04-06-2020.csv
Processing countries, 211 in total.

   Progress =   100.00 %

done
Have a nice day :)
```

It will download the file `MM-DD-YYYY.csv` containing informations about number of total confirmed cases, number of recovered and death cases for each country that are currently presented at the [Worldometer page](https://www.worldometers.info/coronavirus/).

`Contact`
=======

Any questions, comments and/or suggestions are more than welcome at: bojan.vujic@mmk.su.se

Have a nice day! :)

