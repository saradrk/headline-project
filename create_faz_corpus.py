# Sara Derakhshani, 01.02.2021
# Korpus aus Überschriften der FAZ erstellen
# URL und Schleifenparameter müssen angepasst werden
# Suchbegriff variierbar
# HTML-Patters variierbar bzw. müssen evtl. aktualisiert werden


import logging
import requests
from bs4 import BeautifulSoup
import csv

# https://fazarchiv.faz.net/
# Suchbegriff: 'AfD'
# Sucheinstellungen: im Titel, gesamter Zeitraum, alle Ressorts/Quellen, alle Rubriken


logging.basicConfig(filename='create_faz_corpus.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s'
                    )


def month_name_to_nr(name):
    converter = {'Januar': '01',
                 'Februar': '02',
                 'März': '03',
                 'April': '04',
                 'Mai': '05',
                 'Juni': '06',
                 'Juli': '07',
                 'August': '08',
                 'September': '09',
                 'Oktober': '10',
                 'November': '11',
                 'Dezember': '12'
                 }
    return converter[name]


def create_corpus(out_csv):
    url = 'https://fazarchiv.faz.net/fazSearch/index/searchForm?q=AfD&'\
        'search_in=TI&timePeriod=timeFilter&timeFilter=&DT_from=&DT_to=&'\
        'KO%2CSO=&crxdefs=&NN=&CO%2C1E=&CN=&BC=&submitSearch=Suchen&maxHits=&'\
        'sorting=&toggleFilter=&dosearch=new&format=&offset={}#hitlist'
    with open(out_csv, 'w+', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["ID",
                         "JAHR",
                         "MONAT",
                         "TAG",
                         "SPITZMARKE",
                         "ÜBERSCHRIFT",
                         "UNTERÜBERSCHRIFT"
                         ]
                        )
        headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
        n = 1
        max_offset = 4870
        logging.info(f'Start scanning archive of {(max_offset + 10)} articles... ')
        # URL-Parameter: Archiv-Seite 1 == Offset = 0, Seite  + 1 == Offset + 10
        for j in range(0, max_offset, 10):
            req = requests.get(url.format(j), headers)
            soup = BeautifulSoup(req.content, 'html.parser')
            article_teaser = soup.find_all("div", class_="module13")
            for teaser in article_teaser:
                # Datum
                date_banner = teaser.find("div", class_="innerModule1")
                date = date_banner.find("li").get_text()
                month, year = date.split()
                month = month_name_to_nr(month)
                year = year[0:-1]
                headline = teaser.h3.a.get_text()
                # To check wether 'AfD' is in overline or headline or subheading:
                headline_tokens = headline.split()
                # Spitzmarke und Unterüberschrift extrahieren (wenn sie existieren)
                # Spitzmarken-Tag existiert auch ohne Spitzmarkentext (dann leer)
                # Unterüberschriften-Tag nicht
                over_and_sub_header = teaser.find_all("h2")
                # Case subheading and overline exist:
                if len(over_and_sub_header) == 2:
                    # Check if overline h2-tag contains text
                    try:
                        overline = over_and_sub_header[0].get_text()
                        headline_tokens.extend(overline.split())
                    except:
                        logging.info(f'Missing overline on site {((j / 10) + 1)}')
                        overline = None
                    subheading = over_and_sub_header[1].get_text()
                    # Remove subheadings stating the authors:
                    if subheading[0:4] == 'Von ':
                        subheading = None
                    else:
                        headline_tokens.extend(subheading.split())
                # Case only overline exists:
                elif len(over_and_sub_header) == 1:
                    try:
                        overline = over_and_sub_header[0].get_text()
                        headline_tokens.extend(overline.split())
                    except:
                        logging.info(f'Missing overline and subheading on site {((j / 10) + 1)}')
                        overline = None
                    subheading = None
                else:
                    logging.info(f'Problem with overline or subheading on site {((j / 10) + 1)}')
                # Quotes can be included in headline
                afd_tokens = {'AfD', '"AfD"', '"AfD', 'AfD"'}
                if len(afd_tokens.intersection(set(headline_tokens))) > 0:
                    writer.writerow([n,
                                     None,
                                     month,
                                     year,
                                     overline,
                                     headline,
                                     subheading
                                     ]
                                    )
                    n += 1
            if j % 1000 == 0:
                logging.info(f'{j} of {max_offset} articles processed...')
        logging.info('Process finished.')

if __name__ == '__main__':
    create_corpus('afd_headlines_faz.csv')
