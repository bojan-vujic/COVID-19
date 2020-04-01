#!/bin/bash
# https://github.com/bojan-vujic/COVID-19

worldometer="https://www.worldometers.info/coronavirus/"

date=$(date +%m-%d-%Y)

# this will be the name of the csv file
page=$date.csv

tmp="some_file.tmp"  # dummy file that will be deleted at the end.

# directory where the files will be saved.
dir="NEW_daily"

clear



echo "Downloading" $worldometer
echo ""

# First let us download whole page and then do some processing
curl -s $worldometer |                                                     # download the whole page
        sed '1,/Confirmed Cases and Deaths by Country, Territory, or/d' |  # delete all the lines before and including the string
        sed '/Latest Updates/,$d' |                                        # delete all the lines after the string
        sed '1,/>Reported<br/d'   |                                        # the same as first sed command
        sed '/>Country,<br/,$d' > $page                                    # you get the point :)

# Replace all strings in the list with "", practically delete them
for str in Jan Feb Mar Apr; do
  sed -i "s/${str} .*td>//g" $page
done

# Again replace/delete some series of stringsin order to get the table
# I'm positive this is not the best solution, though it works
# if you want to see what each line does, run the script from the very beginning and add each command at the time
echo "Processing the file" $page

sed -i 's/<\/tr>//g
        s/<\/thead>//g
        s/<tbody>//g
        s/<tr style=\"\">//g
        s/<td style=.*px;">//g'   $page  &&  cp $page $tmp && mv $tmp $page  # to avoid some rare issues

# some data are zeros, in such case cell at wordlometer is empty
sed -i 's/><\/td>/>0<\/td>/g
        s/> <\/td>/>0<\/td>/g
        s/>  <\/td>/>0<\/td>/g
        s/ <\/td>/<\/td>/g
        s/  <\/td>/<\/td>/g
        s/<\/a>0<\/td>/<\/td>/g'  $page  &&  cp $page $tmp && mv $tmp $page

sed -i 's/<td style="font-weight: bold; font-size:.*; text-align:left;">/Country : /g
        s/Country : .*country.*">/Country : /g
        s/Country : <span style="color.*">/Country : /g
        /<tr class="total_row">/,$d
        s/<\/tbody>//g'           $page  &&  cp $page $tmp && mv $tmp $page

sed -i '/^$/d'                    $page    # delete all empty lines
sed -i 's/ <td/<td/g
        s/<tr style="background-color.*">//g
        s/ Country/Country/g
         /^[[:space:]]*$/d
        s/<td.*">/<td>/g'         $page  &&  cp $page $tmp && mv $tmp $page

sed -z 's/\n<td>/<td>/g'          $page > $tmp   && mv $tmp $page

sed -i 's/,//g
        s/+//g
        s/<\/td><td>/,/g'         $page  &&  cp $page $tmp && mv $tmp $page

# Now we have almost good csv file
# you can go further with python, I've chosen to stay here for a while

sed -i 's/<\/td>//g
        s/Country : //g
        s/<\/span>0//g
        s/San <td>/San Marino,/g
        s/R\&eacute;union/Reunion/g
        s/Cura\&ccedil;ao/Curacao/g
        s/Bahamas/The Bahamas/g
        s/UK,/United Kingdom,/g
        s/Gambia/The Gambia/g
        s/S. Korea/South Korea/g
        s/USA,/US,/g
        s/Timor-Leste,/East Timor,/g
        s/St. Vincent Grenadines,/Saint Vincent and the Grenadines,/g
        s/UAE,/United Arab Emirates,/g
        s/Congo,/Congo \(Brazzaville\),/g
        s/DRC,/Congo \(Kinshasa\),/g'    $page  &&  cp $page $tmp && mv $tmp $page

# CSV file now have the following form

#  Country  ||   Total   ||   New   ||   Total   ||    New    ||    Total    ||  Active  ||  Serious, ||  Total cases/  ||  Deaths/
#   Other   ||   cases   ||  cases  ||   Deaths  ||   Deaths  ||  Recovered  ||  Cases   ||  Critical ||  1M pop.       ||  1M pop.
#===================================================================================================================================
#   China,       81554,       36,        3312,          7,          76238,        2004,        466,           57,              2


cp $page $tmp

echo "Date\Country,Confirmed,Deaths,Recovered" > $page
num_lines=$(wc -l $tmp | awk '{printf"%i",$1}')
echo "Processing countries," $num_lines "in total."
echo ""


counter=0
while read -r line ; do
  counter=$(( $counter + 1 ))
  country=$(echo         $line | awk -F"," '{print $1}')
  total_cases=$(echo     $line | awk -F"," '{print $2}')
  total_deaths=$(echo    $line | awk -F"," '{print $4}')
  total_recovered=$(echo $line | awk -F"," '{print $6}')
  num=$(echo $line | grep -c "\,")
  echo ${country}","${total_cases}","${total_deaths}","${total_recovered}   >> $page
  perc=$(echo $counter $num_lines | awk '{printf"%8.2f",$1/$2*100}')
  echo -ne "\r   Progress = $perc %"
done < $tmp
mv $page $dir/

rm -f $tmp

echo ""
echo ""
echo "done"
echo "Have a nice day :)"


