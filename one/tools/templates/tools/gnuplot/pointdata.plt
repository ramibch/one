$DATA << EOD
{{ self.data }}
EOD
set key off
set style line 1 linecolor rgb '#0060ad' linetype 1 linewidth 2 pointtype 7 pointsize 1.5
set title "{{ self.title }}"
set xlabel "{{ self.x_label }}"
set ylabel "{{ self.y_label }}"
plot $DATA with linespoints linestyle 1
