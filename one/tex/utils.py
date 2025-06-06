def suggest_margin(papersize):
    if papersize == "a3paper":
        return "2.5cm"
    elif papersize == "a4paper":
        return "2.0cm"
    elif papersize == "a5paper":
        return "1.5cm"
    elif papersize in "letterpaper,legalpaper":
        return "0.75in"
    elif papersize == "ansibpaper":
        return "1.00in"
