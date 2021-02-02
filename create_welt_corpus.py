# Sara Derakhshani, 02.02.2021
# Korpus aus Überschriften der Welt erstellen
# Schleifenparameter müssen aktualisiert werden
# HTML-Patters variierbar bzw. müssen evtl. aktualisiert werden


import logging
import html
import requests
from bs4 import BeautifulSoup
import csv

# https://www.welt.de/schlagzeilen/
# Keine Suche im Archiv möglich: Suche nach 'AfD' erfolgt im Code


logging.basicConfig(filename='create_welt_corpus.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s'
                    )


def create_corpus(out_csv):
    # Add day, month, year
    url = 'https://www.welt.de/schlagzeilen/nachrichten-vom-{}-{}-{}.html'
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
        # headline counter
        n = 1
        logging.info(f'Start scanning archive... ')
        # Search archive by day: Years 2021 - 1995, months Jan. - Dec., days 1-31
        for year in range(2021, 1994, -1):
            logging.info(f'Scanning {year}...')
            for month in range(1, 13):
                logging.info(f'Scanning {month}/{year}...')
                for day in range(1, 32):
                    try:
                        req = requests.get(url.format(day, month, year), headers)
                        soup = BeautifulSoup(req.content, 'html.parser')
                        # Archive can contain text articles, videos and picture galleries
                        # Extract articles: (None if no articles)
                        text_articles = soup.find("div", class_="articles text")
                    except Exception as e:
                        logging.info(f'Problem on {day}.{month}.{year}: {e}')
                        text_articles = None
                    if text_articles:
                        all_headlines = text_articles.find_all("div", class_="text")
                        for headline_teaser in all_headlines:
                            headline = headline_teaser.h4.a.get_text()
                            # To check wether headline contains 'AfD':
                            headline_tokens = headline.split()
                            # Checken ob Spitzmarke existiert (bei älteren Artikeln nicht der Fall)
                            try:
                                overline = headline_teaser.div.h5.get_text()
                                # To check wether overline contains 'AfD':
                                headline_tokens.extend(overline.split())
                            except:
                                overline = None
                            # Search for key word
                            if 'AfD' in set(headline_tokens):
                                # Welt has no subheadings
                                writer.writerow([n,
                                                 day,
                                                 month,
                                                 year,
                                                 overline,
                                                 headline,
                                                 None])
                                n += 1
        logging.info('Process finished.')

if __name__ == '__main__':
    create_corpus('afd_headlines_welt.csv')
