import csv

txt = open('1895-2023.txt', 'r')

with open('US_temperature.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ['year', 'month', 'temperature']
    writer.writerow(field)
    for row in txt:
        words = row.split(',')
        year = words[0][0:4]
        month = words[0][4:6]
        temperature=words[1]
        writer.writerow([year, month, temperature])
    