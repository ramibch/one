$DATA << EOD
{{ self.data }}
EOD
set spiderplot
{% if self.title %}set title "{{ self.title }}"{% endif %}
{% if self.fill %}
set style spiderplot fs transparent solid 0.2 border
{% endif %}
set for [p=1:{{ self.num }}] paxis p range [0:100]
set for [p=2:{{ self.num }}] paxis p tics format ""
set paxis 1 tics font "0,9"
{{ self.render_labels }}
set grid spiderplot
plot for [i=2:{{ self.num_plus_1  }}] $DATA using i:key(1) 