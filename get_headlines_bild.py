# scrape headlines from Bild newspaper archive

import html
import requests
from bs4 import BeautifulSoup
import csv


def main():

    url = 'https://www.bild.de/archive/{}/{}/{}/'
    with open('headlines_bild.csv', 'a', newline='', encoding='utf-8') as csv_file:
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
        errorlist = []
        # Search archive by day: Years 2006 - 2021, months Jan. - Dec., days 1-31
        for year in range(2013, 2022):
            for month in range(1, 13):
                for day in range(1, 32):
                    req = requests.get(url.format(year, month, day), headers)
                    if req.status_code == 404:
                        pass
                    else:
                        soup = BeautifulSoup(req.content, 'html.parser')
                        beginning_of_headlines = soup.find_all('p')[8]
                        headlines = [beginning_of_headlines]
                        sibs = beginning_of_headlines.next_siblings
                        for sib in sibs:
                            headlines.append(sib)


                        for h in headlines:
                            try:
                                #h = h.encode('ascii', 'ignore').decode("utf-8")
                                headline = h.a.get_text()
                                if headline and "AfD" in headline:
                                    n += 1
                                    overline = None
                                    underline = None
                                    writer.writerow([n, year, month, day, overline, headline, underline])
                            except:
                                errorlist.append(h)

        print(len(errorlist))

    return "getting headlines completed"

if __name__ == '__main__':
    print(main())

