import argparse
import logging
logging.basicConfig(level= logging.INFO)
logger = logging.getLogger()

import pandas as pd


def main(filename):
    logger.info('Starting cleaning process')
    df = _read_data(filename)

    main_gender = _extract_gender(filename)
    logger.info(f'Main gender detected: {main_gender}')






def _read_data(filename):
    logger.info('Reading data')
    return pd.read_csv(filename, encoding='utf-8', sep=';')

def _extract_gender(filename):
    logger.info('Extracting main gender')
    return filename.split('_')[0]



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('filename',
                        help= 'The path to the dirty data',
                        type= str)

    args = parser.parse_args()

    df = main(args.filename)

    print(df)
