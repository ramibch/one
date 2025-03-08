$DATA << EOD
#Task start      end
{{ self.data}}
EOD

set xdata time
timeformat = "%Y-%m-%d"
set format x "%b\n'%y"

set yrange [-1:]
OneMonth = strptime("%m","2")
set xtics OneMonth nomirror
set xtics scale 2, 0.5
set mxtics 4
set ytics nomirror
set grid x y
unset key
set title "{{ self.title }}"
set border 3

T(N) = timecolumn(N,timeformat)

set style arrow 1 filled size screen 0.02, 15 fixed lt 3 lw 1.5

plot $DATA using (T(2)) : ($0) : (T(3)-T(2)) : (0.0) : yticlabel(1) with vector as 1, \
     $DATA using (T(2)) : ($0) : 1 with labels right offset -2
