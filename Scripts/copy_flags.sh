
fajl1="log.txt"

mkdir Flags-1 Flags-2

counter=0
while read -r line ; do
  counter=$(( $counter + 1 ))
  if [ "$counter" -lt "100" ] ; then
    dir="Flags-1"
  else
    dir="Flags-2"
  fi
    
  ISO=$(echo $line | awk -F"," '{print $1}')
  ISO3=$(echo $line | awk -F"," '{print $2}')
  echo $counter $ISO $ISO3
  
  cp png/$ISO3.png $dir/$ISO.png
  
  convert $dir/$ISO.png -resize 1000x750 -gravity center \
  -background "rgb(251,252,253)" -extent 1000x750 $dir/$ISO.png
  
  
done < $fajl1