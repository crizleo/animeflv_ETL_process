import argparse
import logging
logging.basicConfig(level= logging.INFO)
logger = logging.getLogger()

import pandas as pd


def main(filename):
    logger.info('Starting cleaning process')
    df = _read_data(filename)

    df = _extract_count_of_genders(df)






def _read_data(filename):
    logger.info('Reading data')
    return pd.read_csv(filename, encoding='utf-8', sep=';')

def _extract_count_of_genders(df):
    logger.info('Counting genders')
    df['nro_generos'] = df['generos'].apply(lambda generos: len(generos.split(' - ')))
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('filename',
                        help= 'The path to the dirty data',
                        type= str)

    args = parser.parse_args()

    df = main(args.filename)

    print(df)
