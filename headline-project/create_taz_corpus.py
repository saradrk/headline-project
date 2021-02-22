import html
import requests
from bs4 import BeautifulSoup
import csv

# taz

# Problem: taz-Archiv funktioniert nur bis ausschließlich Seite 50 (= 999 Artikel)
# Lädt aktuell nur 983/999 Artikel (31.01.21)
# Datum stimmt oft nicht ganz

def main(party):
    """
    party (str): Suchbegriff in korrekter Rechtschreibung (z.B. 'AfD', nicht 'afd')
    """

    url = 'https://taz.de/!s=&Titel={}/?search_page={}'

    with open(party.lower()+'_headlines_taz.csv', 'a', newline='') as csv_file:
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
        # Nur Seiten 0-49 möglich, s.o.
        for j in range(0, 50):
            req = requests.get(url.format(party, j), headers)
            # HTML-Parser erstellen
            soup = BeautifulSoup(req.content, 'html.parser')
            # Artikel
            all_articles = soup.find_all("a", class_=["objlink brief report article leaded noavatar", # normaler Artikel
                                                    "objlink brief subjective commentary article leaded noavatar", # Kommentar
                                                    "objlink brief subjective column article leaded avatar", # Kolumne
                                                    "objlink brief interview article leaded noavatar", # Interview
                                                    "objlink brief legacy article leaded noavatar", # hellgelb hinterlegte Artikel
                                                    "objlink brief legacy article noavatar"]) # hellgelb hinterlegte Artikel ohne Teaser
            # Datum
            all_dates = soup.find_all("li", class_="date")
            for i in range(len(all_articles)):
                article = all_articles[i]

                # Error handling für hellgelb hinterlegte Artikel (haben keine Spitzmarke)
                try:
                    spitzmarke = article.find("h4").text
                except AttributeError:
                    spitzmarke = ''
                # Error handling für "die woche in berlin" (hat manchmal nur die h4-Überschrift...)
                try:
                    headline = article.find("h3").text
                except AttributeError:
                    headline = spitzmarke

                if party in spitzmarke or party in headline:
                    # Datumsformat: '01. 02. 2021'
                    date = all_dates[i].text.split()
                    day = int(date[0][:-1])
                    month = int(date[1][:-1])
                    year = int(date[2])
                    """
                    # Autor*in und Teaser
                    author = soup.find("span", attrs={"class":"author"}).text
                    # Error handling für Artikel ohne Teaser
                    try:
                        teaser = article.find("p").text
                    except AttributeError:
                        teaser = ''
                    """
                    writer.writerow([n+1, year, month, day, spitzmarke, headline, None])
                    n += 1
    return n


if __name__ == '__main__':
    print(main('AfD'))