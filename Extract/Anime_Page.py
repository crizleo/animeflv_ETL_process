import requests
import bs4


class FilteredAnimePage():

    def __init__(self, link):
        self._link = link
        self._html = self._get_html()

    def _get_html(self):
        response = requests.get(self._link)
        response.encoding = 'utf-8'

        response.raise_for_status()

        return bs4.BeautifulSoup(response.text, 'html.parser')

    def _select(self, query_string):
        return self._html.select(query_string)


class AnimeList(FilteredAnimePage):

    def __init__(self, link):
        super().__init__(link)
        try:
            self._next_page = self._select('ul[class="pagination"] li a[rel="next"]')[0]['href']
        except Exception as e:
            self._next_page = '#'

    @property
    def anime_links(self):
        links_list = []
        for link in self._select('ul[class="ListAnimes AX Rows A03 C02 D02"] a'):
            if link and link.has_attr('href'):
                links_list.append(link)
        return set(link['href'] for link in links_list)

    @property
    def next_page(self):
        return self._next_page


class AnimePage(FilteredAnimePage):

    def __init__(self, link):
        super().__init__(link)

    @property
    def nombre(self):
        return self._select('div[class="Ficha fchlt"] div[class="Container"] h1')[0].text

    @property
    def link(self):
        return self._link

    @property
    def sinopsis(self):
        paragraphs = self._select('main[class="Main"] div[class="Description"] p')
        result = '\n'.join([paragraph.text for paragraph in paragraphs])
        return result if len(paragraphs) else ''

    @property
    def estado(self):
        result = self._select('aside[class="SidebarA BFixed"] > p[class*="AnmStts"] > span')
        return result[0].text if len(result) else ''

    @property
    def generos(self):
        generos = self._select('main[class="Main"] nav[class="Nvgnrs"] a')
        result = ' - '.join([genero.text for genero in generos])
        return result if len(result) else ''

    @property
    def puntuacion(self):
        return self._select('div[class="Votes"] span[class="vtprmd"]')[0].text

    @property
    def tipo_produccion(self):
        return self._select('div[class="Ficha fchlt"] div[class="Container"] span[class*="Type"]')[0].text

    @property
    def cantidad_votos(self):
        return self._select('div[class="Votes"] span[id="votes_nmbr"]')[0].text
