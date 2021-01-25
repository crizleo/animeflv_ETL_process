import argparse
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import Anime_Page as ap
import datetime
import csv

def _get_filtered_link(base_link, genero_seleccionado):
    #generamos el link desde donde podemos filtrar para ahorrarnos pasos
    filter_end_point = '/browse?order=title'
    filter_link = base_link+filter_end_point
    option = webdriver.ChromeOptions()
    #algunas opciones
    option.add_argument('--incognito')
    option.add_argument("start-maximized")
    option.add_argument('--disable-dev-shm-usage')
    #abrir el buscador
    driver = webdriver.Chrome(executable_path='C:\chromedriver', options=option)
    #cargar la pagina
    driver.get(filter_link)
    delay = 70
    try:
        WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//button[@class = "multiselect dropdown-toggle btn btn-sm btn-default"]')))
        driver.find_element_by_xpath('//button[@class = "multiselect dropdown-toggle btn btn-sm btn-default"]').click()
        WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//ul[@class = "multiselect-container genres-select dropdown-menu"]/li/a/label')))
        lista_generos = driver.find_elements_by_xpath('//ul[@class = "multiselect-container genres-select dropdown-menu"]/li')
        generos = [genero.find_element_by_xpath('.//input').get_attribute('value').replace('-', '_') for genero in lista_generos]
    except TimeoutException:
        print('Error: La pagina tardo demasiado en cargar')
    #seleccionar el genero
    for i, genero in enumerate(generos):
        if genero == genero_seleccionado:
            lista_generos[i].click()
    driver.find_element_by_xpath('//button[@class = "btn btn-sm btn-primary"]').click()
    #obtenemos el link actual
    filtered_link = driver.current_url
    #cerramos el navegador
    driver.close()
    #devolvemos el link con los filtros aplicados
    return filtered_link

def _anime_scraper(filtered_link, base_link):
    filtered_anime_page = ap.AnimeList(filtered_link)
    animes = []
    while filtered_anime_page.next_page != '#':
        for anime_link in filtered_anime_page.anime_links:
            try:
                anime = ap.AnimePage(base_link+anime_link)
                if anime:
                    print(f'opteniendo informacion de {anime.nombre}')
                    print(base_link + anime_link)
                    animes.append(anime)
                else:
                    print(f'Error extrayendo {base_link+anime_link}')
            except (HTTPError, MaxRetryError):
                print(f'Error: no se pudo obtener {base_link+anime_link}')
        filtered_anime_page = ap.AnimeList(base_link+filtered_anime_page.next_page)
    _save_animes(animes)

def _save_animes(animes):
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = f'animeflv_{now}_articles.csv'

    csv_headers = list(filter(lambda property: not property.startswith('_'), dir(animes[0])))

    with open(out_file_name, mode='w+', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(csv_headers)

        for anime in animes:
            row = [str(getattr(anime, prop))for prop in csv_headers]
            writer.writerow(row)

if __name__ == '__main__':
    base_link = 'https://www3.animeflv.net'

    parser = argparse.ArgumentParser()

    #lista de opciones
    generos_disponibles = ['accion', 'artes_marciales', 'aventura', 'carreras', 'ciencia_ficcion', 'comedia', 'demencia', 'demonios', 'deportes', 'drama', 'ecchi', 'escolares', 'espacial', 'fantasia', 'harem', 'historico', 'infantil', 'josei', 'juegos', 'magia', 'mecha', 'militar', 'misterio', 'musica', 'parodia', 'policia', 'psicologico', 'recuentos_de_la_vida', 'romance', 'samurai', 'seinen', 'shoujo', 'shounen', 'sobrenatural', 'superpoderes', 'suspenso', 'terror', 'vampiros', 'yaoi', 'yuri']

    parser.add_argument('genero',
                        help = 'las opciones son',
                        type = str,
                        choices= generos_disponibles)

    args = parser.parse_args()

    filtered_link = _get_filtered_link(base_link, args.genero)

    _anime_scraper(filtered_link, base_link)




