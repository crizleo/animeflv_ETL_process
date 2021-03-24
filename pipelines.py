import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import subprocess

generos = ['accion', 'artes_marciales', 'aventura', 'carreras', 'ciencia_ficcion', 'comedia',
           'demencia', 'demonios', 'deportes', 'drama', 'ecchi', 'escolares', 'espacial',
           'fantasia', 'harem', 'historico', 'infantil', 'josei', 'juegos', 'magia', 'mecha',
           'militar', 'misterio', 'musica', 'parodia', 'policia', 'psicologico', 'recuentos_de_la_vida',
           'romance', 'samurai', 'seinen', 'shoujo', 'shounen', 'sobrenatural', 'superpoderes',
           'suspenso', 'terror', 'vampiros', 'yaoi', 'yuri']

def main():
    _extract()
    _transform()

def _extract():
    logger.info("Starting extract process\n")
    for genero in generos:
        logger.info(f'Extracting {genero}')
        subprocess.run(['python', 'main.py', genero], cwd="./extract")
        subprocess.run(['find', '.', '-name', f'animeflv_{genero}*',
                        '-exec', 'mv', '{}', f'../transform/{genero}.csv', ';'], cwd= './extract')

def _transform():
    logger.info('Starting transform process')
    for genero in generos:
        subprocess.run(['python', 'recipe.py', f'{genero}.csv'])


if __name__ == "__main__":
    main()