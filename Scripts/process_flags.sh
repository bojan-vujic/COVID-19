

dir=globe
dir2=changed_images

mkdir -p $dir2

images=$(ls $dir)

for image in $images; do
  
  
  cp $dir/$image $dir2/$image
  
  convert $dir2/$image -resize 1000x750 -gravity center \
  -background "rgb(251,252,253)" -extent 1000x750 $dir2/$image
  echo $image
  
done