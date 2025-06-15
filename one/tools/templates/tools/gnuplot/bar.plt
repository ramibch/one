$DATA << EOD
{{ self.render_data }}
EOD
set boxwidth 0.5
set key off
set style fill solid
set title "{{ self.title }}"
plot $DATA using 1:3:xtic(2) with boxes
