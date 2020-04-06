#!/bin/bash
# https://github.com/bojan-vujic/COVID-19

worldometer="https://www.worldometers.info/coronavirus/"

# $bash covid-19.sh
# date is today

# $bash covid-19.sh 1
# date is yesterday

# It is intended in case when downloading data for today after 00:00,
# so that you won't have to change date manually.
if [ $# -eq 0 ] ; then
  date=$(date +%m-%d-%Y)
else
  date=$(date -d "$1 day ago" '+%m-%d-%Y')
fi

# this will be the name of the csv file
csv=$date.csv
html=$date.html

# dummy file that will be deleted at the end.
tmp="some_file.tmp"

# folders where the files will be saved.
dir="CSV_data/Daily_csv"
dir2="CSV_data/Github"
dir3="CSV_data/HTML"

mkdir -p $dir
mkdir -p $dir2
mkdir -p $dir3

clear
echo "Downloading" $worldometer
echo ""

# First, let us download the whole page and then do some processing.
# Original html file will be saved intact, just in case if
# the following processing doesn't work correctly.
# Sometimes people from worldometer page change their page slightly,
# then this script have to be updated accordingly.
curl -s $worldometer  >  $dir3/${date}_org.html                   # download the whole original html page.

# copy the original html as a new html file that will be slightly
# processed so that can be quickly loaded in browser
cp $dir3/${date}_org.html $html

echo "Processing the file" $html

sed -z 's/<td style="font-weight: bold; \+\n/<td style=\"font-weight: bold; /g'    $html  > $tmp  &&  mv $tmp $html

# Replace some more characters that wont change the nature of html file,
# it will make next part of the job a lot easier.
sed -i 's/;"/"/g'                              $html
sed -i 's/   \+.*text-align:/ text-align:/g'   $html

sed -i -e 's/right"> \+<\/td>/right"><\/td>/'  $html

# Some cells are empty, the data are equal to zero, so we will replace those empty cells with zeros.
# Also, we will remove all "+" and "," characters from the file.
sed -i 's/right"><\/td>/right">0<\/td>/g
        s/,//g
        s/+//g'                                $html

# Html contains the data for today and yesterday.
# Using these two lines, we will take both of them.
# Separation and cleaning is quite intuitive, yet a bit long, as you will see.

# Delete all the lines before and including the string.
# This assumes that strings "Yesterday" and "Highlighted in green"
# are appearing only once in the file.
sed -i '1,/Yesterday/d'             $html

# delete all the lines after and including the string
sed -i '/Highlighted in green/,$d'  $html

echo "Converting html file using html2txt."
html2text   -style pretty  $html > $csv
mv $html $dir3/

# Replace all the empty spaces into commas, to create comma separated file, csv.
sed -i 's/ \+/,/g'   $csv

# Replace some string at specific line number in the file.
# If larger number of cases, we could use a loop. Not needed in present case.
ln1=$(grep -n "Macedonia"   $csv | head -1 | awk -F: '{print $1 - 1}')
ln2=$(grep -n "Macedonia"   $csv | tail -1 | awk -F: '{print $1 - 1}')
sed -i 's/Macedonia//g'  $csv
sed -i "${ln1}s/North,/North Macedonia,/"  $csv
sed -i "${ln2}s/North,/North Macedonia,/"  $csv

ln1=$(grep -n "Caribbean,"   $csv | head -1 | awk -F: '{print $1 + 1}')
ln2=$(grep -n "Caribbean,"   $csv | tail -1 | awk -F: '{print $1 + 1}')
sed -i "${ln1}s/Netherlands//"  $csv
sed -i "${ln2}s/Netherlands//"  $csv

ln1=$(grep -n "Equatorial,"   $csv | head -1 | awk -F: '{print $1 + 1}')
ln2=$(grep -n "Equatorial,"   $csv | tail -1 | awk -F: '{print $1 + 1}')
sed -i "${ln1}s/Guinea//"  $csv
sed -i "${ln2}s/Guinea//"  $csv

# Use sed to replace some country name related things.
sed -i 's/_/ /g
        s/Caribbean,/Caribbean Netherlands,/g
        s/Republic//g
        s/USA,/US,/g
        s/UK,/United Kingdom,/g
        s/S. Korea/South Korea/g
        s/Dominican/Dominican Republic/g
        s/UAE,/United Arab Emirates,/g
        s/MS,Zaandam,/MS Zaandam,/g
        s/Réunion,/Reunion,/g
        s/Princess//g
        s/Diamond,/Diamond Princess,/g
        s/Herzegovina//g
        s/Bosnia and,/Bosnia and Herzegovina,/g
        s/DRC,/Congo \(Kinshasa\),/g
        s/Tobago//g
        s/Trinidad and,/Trinidad and Tobago,/g
        s/Polynesia//g
        s/French,/French Polynesia,/g
        s/Barbuda//g
        s/Antigua and,/Antigua and Barbuda,/g
        s/and Nevis//g
        s/Saint Kitts,/Saint Kitts and Nevis,/g
        s/Congo,/Congo \(Brazzaville\),/g
        s/Grenadines//g
        s/St. Vincent,/Saint Vincent and the Grenadines,/g
        s/Bahamas,/The Bahamas,/g
        s/Caicos//g
        s/Turks and,/Turks and Caicos,/g
        s/Timor-Leste,/East Timor,/g
        s/CAR,/Central African Republic,/g
        s/Sahara//g
        s/Western,/Western Sahara,/g
        s/Gambia,/The Gambia,/g
        s/Equatorial,/Equatorial Guinea,/g
        s/Curaçao/Curacao/g
        s/Papua New,/Papua New Guinea,/g
        s/Miquelon//g
        s/Saint Pierre,/Saint Pierre Miquelon,/g
        s/Country,.*//g
        s/Other,Cases,.*//g
        s/Total:,.*//g
        s/Islands//g
        s/Channel,/Channel Islands,/g
        s/Faeroe,/Faeroe Islands,/g
        s/Cayman,/Cayman Islands,/g
        s/British//g
        s/Virgin,/British Virgin Islands,/g
        s/Falkland,/Falkland Islands,/g
        s/Cruise Ship.*//g
        s/Brunei ,/Brunei,/g'         $csv

ln1=$(grep -n "Papua New Guinea,"   $csv | head -1 | awk -F: '{print $1 + 1}')
ln2=$(grep -n "Papua New Guinea,"   $csv | tail -1 | awk -F: '{print $1 + 1}')
sed -i "${ln1}s/Guinea//"  $csv
sed -i "${ln2}s/Guinea//"  $csv

# use awk to replace all the empty lines
awk 'NF'  $csv  > $tmp  &&  mv $tmp $csv

# Insert a new line in front of a pattern
ln1=$(grep -n "World,"   $csv | head -1 | awk -F: '{print $1 - 1}')
sed -i 's/World,/\nCurrent data (today)\n\n&/g'   $csv

# Now we have almost good csv file
# you can go further with python, I've chosen to stay here just for a little while.

ln1=$(grep -n "Current data (today)"   $csv | tail -1 | awk -F: '{print $1}')
sed -i "${ln1}s/Current data (today)/Data for yesterday/"    $csv

sed -i 's/World,.*//g'    $csv


# copy file with 2 tables containing the data for today and yesterday
cp $csv $dir3/${date}_2-tables.csv

sed -i 's/Current data.*//g'  $csv
awk 'NF'  $csv  > $tmp  &&  mv $tmp $csv


# delete all the lines after the string
sed -i '/Data for yesterday/,$d'  $csv

# Cat csv file and save only specific columns from it.
cat $csv | awk -F"," '{print $1","$2","$4","$6","$8}'  >  $tmp  &&  mv $tmp $csv


# CSV file now have the following form

#  Country  ||   Total   ||   Total   ||    Total    ||  Serious, ||
#   Other   ||   cases   ||   Deaths  ||  Recovered  ||  Critical ||
#===================================================================
#   China,       81669,       3329,         76964,         295,     

# This awk one liner will find sum of each column (World data) and append it to csv.
awk -F"," '{for(i=2; i<=NF; i++) a[i] += $i; print $0} END {l="World"; i=2; while(i in a){l=l","a[i]; i++};print l}' $csv > $tmp


echo "Date\Country,Confirmed,Deaths,Recovered" > $csv
echo "Date\Country,Confirmed,Deaths,Recovered,Critical" > ${date}_ALL.csv
echo "Date\Country,Critical" > ${date}_Critical.csv
num_lines=$(wc -l $tmp | awk '{printf"%i",$1}')
echo "Processing countries," $num_lines "in total."
echo ""

# There is a faster way of doing this.
# I like this approach. If you don't, you could use:
# cat $csv | awk '{print tables that you want}' > some_output_file (confirmed, recovered, ...)

counter=0
while read -r line ; do
  counter=$(( $counter + 1 ))
  country=$(echo         $line | awk -F"," '{print $1}')
  total_cases=$(echo     $line | awk -F"," '{print $2}')
  total_deaths=$(echo    $line | awk -F"," '{print $3}')
  total_recovered=$(echo $line | awk -F"," '{print $4}')
  critical=$(echo        $line | awk -F"," '{print $5}')
  num=$(echo $line | grep -c "\,")
  echo ${country}","${total_cases}","${total_deaths}","${total_recovered}  >> $csv
  echo ${country}","${total_cases}","${total_deaths}","${total_recovered}","${critical}  >> ${date}_ALL.csv
  echo ${country}","${critical}   >> ${date}_Critical.csv
  perc=$(echo $counter $num_lines | awk '{printf"%8.2f",$1/$2*100}')
  echo -ne "\r   Progress = $perc %"
done < $tmp
mv $csv $dir/
cp ${date}_Critical.csv $dir2/
mv ${date}_Critical.csv $dir/
mv ${date}_ALL.csv $dir/
rm -f $tmp

echo ""
echo ""
echo "done"
echo "Have a nice day :)"

# this part is optional, either do it here, or in command line, or via jupyter notebook.
# It is better do do it first in command line, to make sure you have all the python packages installed.
python3.6 1-COVID-19_Process_daily_file_from_Worldometer.py $date


