import html
import requests
from bs4 import BeautifulSoup
import csv

# Junge Freiheit
# Seitenzahl auf der Website geht nur bis 300, es funktioniert aber aktuell bis 445 (31.01.21)

# Problem: 1-10 Artikel fehlen

def main(party, pages):
    """
    party (str): Suchbegriff in korrekter Rechtschreibung (z.B. 'AfD', nicht 'afd')
    pages (int): Wie viele Seiten Treffer es für diesen Suchbegriff gibt
    """

    # Erster Artikel vom 01.03.2013
    url = 'https://jungefreiheit.de/page/{}/?s={}'
    months_conversion = {'Januar': 1, 'Februar': 2, 'März': 3, 'April': 4, 'Mai': 5, 'Juni': 6, 'Juli': 7,
                        'August': 8, 'September': 9, 'Oktober': 10, 'November': 11, 'Dezember': 12}

    with open(party.lower()+'_headlines_jf.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["ID", "JAHR", "MONAT", "TAG", "SPITZMARKE", "ÜBERSCHRIFT", "UNTERÜBERSCHRIFT"])
        
        headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-wir Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }

        n = 0
        # SEITE 
        for j in range(1, pages+1):
            req = requests.get(url.format(j, party), headers)
            # HTML-Parser erstellen
            soup = BeautifulSoup(req.content, 'html.parser')
            # Artikel
            all_articles = soup.find_all("h3", class_="elementor-post__title")
            # Datum
            all_dates = soup.find_all("span", class_="elementor-post-date")

            for i in range(len(all_articles)):
                article = all_articles[i]

                try:
                    headline = article.find("h2", class_="ee-post__title__heading").text
                    spitzmarke = article.find("h3", class_="subheadline").text
                # Error handling für "JUNGE FREIHEIT EXKLUSIV"
                except AttributeError:
                    headline = article.text.strip()
                    spitzmarke = ''

                # Nur in Datei schreiben, wenn Suchbegriff in Spitzmarke oder Überschrift
                if party in spitzmarke or party in headline:
                    # Datumsformat: '1. Februar 2021'
                    date = all_dates[i].text.split()
                    assert len(date) == 3
                    day = int(date[0][:-1])
                    month = months_conversion[date[1]]
                    year = int(date[2])
                    writer.writerow([n+1, year, month, day, spitzmarke, headline, None])
                    n += 1
    return n


if __name__ == '__main__':
    print(main('AfD', 445))