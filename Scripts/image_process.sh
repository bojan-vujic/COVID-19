#!/bin/bash

# This script will process images from folder Maps and save them in changed_images
dir=Maps
dir2=changed_images

mkdir -p $dir2

images=$(ls $dir)

#yellow=rgb(255,255,0)
dark_purple="rgb(95,0,95)"
bckg="rgb(219,223,239)"
bckg="rgb(251,252,253)"

for image in $images; do
  # convert white to transparent
  convert  $dir/$image  -transparent white $dir2/$image
  
  # convert main color to some other
  convert $dir2/$image +level-colors "${dark_purple}", $dir2/$image
  
  # convert transparent background to some other
  convert $dir2/$image \
  -background "${bckg}" \
  -alpha remove \
  -flatten \
  -alpha on \
  $dir2/$image
  echo $image

done
