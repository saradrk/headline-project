# scrape headlines from Bild newspaper archive

import html
import requests
from bs4 import BeautifulSoup
import csv
import re


def main():

    url = 'https://www.bild.de/archive/{}/{}/{}/'
    with open('bild_alle_parteien.csv', 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["ID", "PARTEINAME", "JAHR", "MONAT", "TAG",  "ÜBERSCHRIFT"])
        headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }

        print("getting headlines...")

        party_n = 0
        ges_n = 0
        # Search archive by day: Years 2013 - 2021, months Jan. - Dec., days 1-31
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
                            ges_n += 1
                            headline = h.a.get_text()
                            parties = ["AfD", "SPD", "CDU", "CSU", "FDP", "Grüner?n?\x20(?!Woche)", "Link(?!\x20)er?n?|Linkspartei"]
                            for party in parties:
                                p = re.search(party, headline)
                                if p:
                                    party_n += 1
                                    if party == "Grüner?n?\x20(?!Woche)":
                                        party = "Bündnis 90/Die Grünen"
                                    elif party == "Link(?!\x20)er?n?|Linkspartei":
                                        party = "Die Linke"
                                    else:
                                        pass
                                    if party == "CDU" or party == "CSU":
                                        party = "CDU/CSU"
                                    writer.writerow([party_n, party, year, month, day, headline, ])


        print(ges_n)

    return "getting headlines completed"

if __name__ == '__main__':
    print(main())

