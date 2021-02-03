# scrape headlines from compact newspaper archive

import html
import requests
from bs4 import BeautifulSoup
import csv
import re


def main():

    url = 'https://www.sueddeutsche.de/news/page/{}?search=afd&sort=date&all%5B%5D=dep&all%5B%5D=typ&all%5B%5D=sys&all%5B%5D=time'
    with open('headlines_sueddeutsche.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["ID", "JAHR", "MONAT", "TAG", "SPITZMARKE", "ÜBERSCHRIFT", "UNTERÜBERSCHRIFT"])
        headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }

        print("getting headlines...")

        n = 0
        for j in range(1,101):
            req = requests.get(url.format(j), headers)
            soup = BeautifulSoup(req.content, 'html.parser')
            overlines = soup.find_all("strong", class_ = "entrylist__overline") # Überüberschrift
            headlines = soup.find_all("em", class_="entrylist__title")  # Überschrift
            dates_times = soup.find_all("time", class_="entrylist__time")
            #ressorts = soup.find_all("a", class_ = "entrylist__link")

            for i in range(len(headlines)):

                #ressort = str(ressorts[i]).split('/')[3]
                headline = headlines[i].get_text()
                overline = overlines[i].get_text()
                underline = None
                date_time = dates_times[i].get_text()
                if re.match(r'^\d{2}\.\d{2}\.\d{4}$', date_time[5:15]):
                    year = date_time[11:15]
                    month = date_time[8:10]
                    day = date_time[5:7]
                else:
                    year = None
                    month = None
                    day = None
                if overline != "SZ-Magazin":
                    if "AfD" in overline or "AfD" in headline:
                        n += 1
                        writer.writerow([n, year, month, day, overline, headline, underline])


        return "getting headlines completed"

if __name__ == '__main__':
    print(main())