import csv

txt = open('snow_cover.txt', 'r')

with open('snow_cover.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ['year', 'month', 'coverage']
    writer.writerow(field)
    for row in txt:
        words = row.split()
        year = words[0]
        month = words[1]
        area=words[2]
        writer.writerow([year, month, area])
    