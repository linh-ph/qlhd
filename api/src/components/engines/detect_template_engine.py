def get_detect_template(url):
    number_template = 0
    url = url.lower()
    if "(85)" in url:
        number_template = 1
    if "(91)" in url:
        number_template = 2
    if "(95)" in url:
        number_template = 3
    if "(99)" in url:
        number_template = 4
    if "(100)" in url:
        number_template = 5

    return number_template
