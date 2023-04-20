#!/bin/bash
selected_text="$(xsel -o)"
# fare konumunu al
xy=$(xdotool getmouselocation)

# x ve y koordinatlarına ayır
x=$(echo $xy | awk '{print $1}' | awk -F: '{print $2}')
y=$(echo $xy | awk '{print $2}' | awk -F: '{print $2}')

echo $x

if [ ! -z "$selected_text" ]; then
    python3 /home/bismih/projelerimiz/bash/ceviri/cevir.py "$selected_text" $x $y
fi