#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
import logging

logging.basicConfig(filename='compute_frequencies.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s'
                    )


def main(path):
    with open('frequency_analyses.csv', 'w+', encoding='utf-8') as out_csv:
        writer = csv.writer(out_csv)
        writer.writerow(["newspaper",
                         "n_headlines",
                         "n_overlines",
                         "n_sublines",
                         "av_word_count",
                         "av_word_length"
                         ]
                        )
        for file in os.listdir(path):
                if file.endswith(".csv"):
                    path_to_file = os.path.join(path, file)
                    print(path_to_file)
                    with open(path_to_file, 'r', encoding='utf-8') as newspaper_csv:
                        reader = csv.DictReader(newspaper_csv)
                        # get newspaper name from filename
                        newpaper = file.split('_')[2][0:-4]
                        word_count = 0
                        headline_counter = 0
                        overline_counter = 0
                        subline_counter = 0
                        char_counter = 0
                        for row in reader:
                            try:
                                # word length for word in headline
                                hl_word_length = [len(word) for word in row['ÜBERSCHRIFT'].split()]
                                word_count += len(hl_word_length)
                                char_counter += sum(hl_word_length)
                                headline_counter += 1
                                if row['SPITZMARKE']:
                                    # word length for word in overline
                                    ol_word_length = [len(word) for word in row['SPITZMARKE'].split()]
                                    word_count += len(ol_word_length)
                                    char_counter += sum(ol_word_length)
                                    overline_counter += 1
                                if row['UNTERÜBERSCHRIFT']:
                                    # word length for word in subline
                                    sl_word_length = [len(word) for word in row['UNTERÜBERSCHRIFT'].split()]
                                    word_count += len(sl_word_length)
                                    char_counter += sum(sl_word_length)
                                    subline_counter += 1
                            except Exception as e:
                                logging.info('Error in {file} headline no. {headline_counter}. {e}')
                        writer.writerow([newpaper,
                                         headline_counter,
                                         overline_counter,
                                         subline_counter,
                                         round((word_count/headline_counter), 2),
                                         round((char_counter/word_count), 2)
                                         ]
                                        )



if __name__ == '__main__':
    main('local/data/csv/')

