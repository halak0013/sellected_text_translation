#!/bin/bash
selected_text="$(xsel -o)"
location=$(dirname "$0")
# get mouse position
xy=$(xdotool getmouselocation)

# split x and y coordinates
x=$(echo $xy | awk '{print $1}' | awk -F: '{print $2}')
y=$(echo $xy | awk '{print $2}' | awk -F: '{print $2}')

echo $x

if [ ! -z "$selected_text" ]; then
    python3 $location/cevir.py "$selected_text" $x $y
fi