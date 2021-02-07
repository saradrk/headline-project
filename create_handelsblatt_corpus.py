#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sara Derakhshani, 02.02.2021
# Korpus aus Überschriften des Handelsblatt erstellen
# Schleifenparameter müssen aktualisiert werden
# HTML-Patters variierbar bzw. müssen evtl. aktualisiert werden

import logging
import html
import requests
from bs4 import BeautifulSoup
import csv

# https://www.handelsblatt.com/suche/
# Suchbegriff: 'AfD'
# Sucheinstellungen: Ressorts (alle), Dokumententyp (Artikel)


logging.basicConfig(filename='create_handelsblatt_corpus.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s'
                    )


def create_corpus(out_csv):
    url = 'https://www.handelsblatt.com/suche/?p3616352={}&sw=AfD&'\
        'search-ressort=-1&search-doctype=article&search-authorids='\
        '-1&search-sort=date'
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
        archive_sites_n = 653
        logging.info(f'Start scanning archive of {(archive_sites_n*10)} articles... ')
        for j in range(n, archive_sites_n):
            req = requests.get(url.format(j), headers)
            soup = BeautifulSoup(req.content, 'html.parser')
            article_teaser = soup.find_all("a", class_="vhb-teaser-link")
            for teaser in article_teaser:
                # Datum
                date = teaser.time.string
                day, month, year = date.split('.')
                headline_tag = teaser.find("div", class_="vhb-teaser-head")
                # Spitzmarke
                overline = headline_tag.em.get_text()
                # Überschrift
                headline = headline_tag.find("span", class_="vhb-headline").get_text()
                # Check wether 'AfD' is in overline or headline or subheading
                # if yes add to csv
                complete_teaser_text = headline
                try:
                    overline = headline_tag.em.get_text()
                    complete_teaser_text = complete_teaser_text + ' ' + overline
                except Exception as e:
                    logging.warning(f'Problem with getting overline on site {j}: {e}')
                    overline = None
                try:
                    subheading = teaser.p.get_text()
                    # Remove 'Mehr…' and following authors
                    end_pos = subheading.find("Mehr…") - 1
                    subheading = subheading[0:end_pos]
                    complete_teaser_text = complete_teaser_text + ' ' + subheading
                except Exception as e:
                    logging.warning(f'Problem with getting subheading on site {j}: {e}')
                    subheading = None
                # Quotes can be included in headline
                if 'AfD' in complete_teaser_text:
                    writer.writerow([n,
                                     day,
                                     month,
                                     year,
                                     overline,
                                     headline,
                                     subheading])
                    n += 1
            if j % 100 == 0:
                logging.info(f'{(j * 10)} of {(archive_sites_n * 10)} articles processed...')
        logging.info('Process finished.')

if __name__ == '__main__':
    create_corpus('afd_headlines_handelsblatt.csv')
