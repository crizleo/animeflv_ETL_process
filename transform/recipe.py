import argparse
import logging
logging.basicConfig(level= logging.INFO)
logger = logging.getLogger()

import pandas as pd


def main(filename):
    logger.info('Starting cleaning process\n')
    df = _read_data(filename)

    df = _extract_count_of_genders(df)

    df = _remove_duplicated_entries(df)

    df = _drop_rows_with_missing_values(df)

    _save_data(df, filename)

    return df



def _read_data(filename):
    logger.info('Reading data')
    return pd.read_csv(filename, encoding='utf-8', sep=';')

def _extract_count_of_genders(df):
    logger.info('Counting genders\n')
    df['nro_generos'] = df['generos'].apply(lambda generos: len(generos.split(' - ')))
    return df

def _remove_duplicated_entries(df):
    logger.info('Removing duplicated entries\n')
    df = df.drop_duplicates(subset='column', inplace=True, keep='first')
    return df

def _drop_rows_with_missing_values(df):
    logger.info('Removing rows with missing values')
    return df.dropna()

def _save_data(df, filename):
    clean_filename = f'clean_{filename}'
    logger.info(f'saving data at location: {clean_filename}')
    df.to_csv(filename= clean_filename, sep=';', encoding='utf-8')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('filename',
                        help= 'The path to the dirty data',
                        type= str)

    args = parser.parse_args()

    df = main(args.filename)

    print(df)
