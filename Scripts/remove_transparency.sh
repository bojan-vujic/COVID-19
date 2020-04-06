

dir=iso_code_maps
dir2=changed_figures

mkdir $dir2

images=$(ls $dir)
#yellow=rgb(255,255,0)
dark_purple="rgb(95,0,95)"
pozadina="rgb(219,223,239)"
pozadina="rgb(251,252,253)"
#pozadina="white"

counter=0
for image in $images; do
  counter=$(( $counter + 1 ))
  
  if [[ "$counter" -lt "100" ]] ; then
    dir2="1-changed_figures"
  else
    dir2="2-changed_figures"
  fi
  
  # convert white to transparent
  convert  $dir/$image  -transparent white $dir2/$image
  
  # convert main color to some other
  convert $dir2/$image +level-colors "${dark_purple}", $dir2/$image
  
  # convert transparent background to some other
  convert $dir2/$image \
  -background "${pozadina}" \
  -alpha remove \
  -flatten \
  -alpha on \
  $dir2/$image
  echo $image

done
