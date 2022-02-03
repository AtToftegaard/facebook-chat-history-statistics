import csv
from bs4 import BeautifulSoup

def write_to_csv(filename):
    csvfile = csv.writer(open("messages.csv", "w"))
    csvfile.writerow(["date"])
    with open(filename) as fp:
        soup = BeautifulSoup(fp, 'lxml')
    dates = soup.findAll('span', {'class' : 'meta'})
    for date in dates:
        data = date.contents[0].split(",", 1)
        data = data[1].split("at")
        data = str(data[0])
        data = data.split(",")
        data = " ".join(data)
        data = data.split(" ")
        data = " ".join(data)
        csvfile.writerow([data])