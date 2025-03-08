set title "{{ self.title }}"
unset key
set tic scale 0

# Color runs from white to green
set palette rgbformula -7,2,-7
unset cbtics

$map1 << EOD
{{ self.data }}
EOD

set view map
splot '$map1' matrix with image
