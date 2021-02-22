import html
import requests
from bs4 import BeautifulSoup
import csv

# Neues Deutschland

# Problem: ND-Archiv zeigt max. 100 Artikel auf einmal an, man muss also über Datum filtern
# Suche funktioniert nicht richtig; es werden auch Artikel außerhalb der Datumsgrenzen angezeigt
# => Artikel werden mehrfach in csv geschrieben, Postprocessing nötig

# year_end = 2022 = alles von year_start bis heute
def main(party, search_year_start, search_year_end=2021):
    """
    party (str): Suchbegriff in korrekter Rechtschreibung (z.B. 'AfD', nicht 'afd')
    search_year_start (int): Jahr, ab dem gesucht werden soll
    search_year_end (int): Jahr, bis zu (inkl.) dem gesucht werden soll. Default 2021
    """
    # URL entspricht der Suche in Spitzmarke, Überschrift + Unterüberschrift; nicht Autor*in/Inhalt
    url = 'https://www.neues-deutschland.de/suche/index.php?start={}&search=1&and={}&modus=2&s0_y={}&s0_m={}&s0_d={}&s1_y={}&s1_m={}&s1_d={}&sort=1&display=1&searchfields%5B0%5D=0&searchfields%5B1%5D=1&searchfields%5B2%5D=2'

    with open(party.lower()+'_headlines_nd.csv', 'a', newline='') as csv_file:
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
        # Überschriften, die in csv geschrieben werden, hier speichern,
        # um doppelte Artikel auszusortieren
        written_headlines = set()
        # JAHR
        for search_year in range(search_year_start, search_year_end+1):
            # MONAT
            for search_month in range(1, 13):
                # TAG
                # day = 1, 11, 21, 31 (url.format() unten macht 10-Tages-Schritte)
                # Es wird also erst 1.-11., dann 12.-22., dann 23.-33. ausgelesen
                for search_day in range(1, 32, 11):
                    # SEITE
                    # Seiten durchblättern: Archiv spuckt max. 100 Artikel auf einmal aus
                    # 10 Artikel pro Seite = max. 10 Seiten
                    # Seitennavigation in 10er Schritten (0-90)
                    # Leere Seiten enthalten nur die h3-Überschrift "__ Artikel gefunden",
                    # breaken also nicht den Code
                    for j in range(0, 100, 10):
                        # Format: Seitennummer, Suchanfrage, Jahr (von), Monat (von), Tag (von),
                        #         Jahr (bis), Monat (bis), Tag (bis = von+10)
                        req = requests.get(url.format(j, party, search_year, search_month, search_day, 
                                                      search_year, search_month, search_day+9), 
                                           headers)
                        # HTML-Parser erstellen
                        soup = BeautifulSoup(req.content, 'html.parser')
                        all_headlines = soup.find_all("h3")
                        # Überschrift "__ Artikel gefunden" löschen
                        all_headlines = all_headlines[1:]
                        all_teasers = soup.find_all("p", class_="Teaser") # Datum + Teaser
                        all_spitzmarken = soup.find_all("div", class_="Deck") # Spitzmarke + Ressort
                        for i in range(len(all_headlines)):
                            # Überschrift aus Link auslesen
                            headline = all_headlines[i].a.string
                            if party in headline and headline not in written_headlines:
                                """
                                # Artikelvorschau
                                teaser = all_teasers[i].contents[-1].strip()
                                """
                                # 1 Element in all_teasers: ['\n', DATUM, ARTIKELVORSCHAU]
                                # Datumsformat: '01.02.2021'
                                date = all_teasers[i].contents[1].get_text().split('.')
                                article_day, article_month, article_year = [int(i) for i in date]
                                spitzmarke = all_spitzmarken[i].find("span", class_="Kicker")
                                # Nicht alle Artikel haben Spitzmarken (manche haben None)
                                if spitzmarke:
                                    spitzmarke = spitzmarke.text
                                # n+1 um mit id=1 zu beginnen
                                writer.writerow([n+1, article_year, article_month, article_day, spitzmarke, headline, None])
                                written_headlines.add(headline)
                                n += 1
    return n


if __name__ == '__main__':
    print(main('AfD', 2013))