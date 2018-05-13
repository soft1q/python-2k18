'''
 Parsing module on project "Telegram Bot"
 Parses given input (article or link to it``)
 Version: beto 1.0
 Creator: Levashov Artem, MIPT DIHT 790, 2018
'''


from bs4 import BeautifulSoup
import requests
import wikipedia
import wikia


class InvalidInput(Exception):
    def __init__(self, string):
        self.error_text = 'Tried create Article object on {}'.format(string)


class PageNotFound(Exception):
    def __init__(self, wiki, title):
        self.error_text = 'Cannot find page with ' \
                          'title {} in wiki {}'.format(title, wiki)


def get_lang_wiki(url_list):
    '''Getting wiki and language from parted by '/' url'''
    for url_part in url_list:
        item = url_part.split('.')
        if 'wikipedia' in item or 'wikia' in item:
            return item[1], item[0]


def get_article_name(link):
    '''Parsing HTML page for article header'''
    req = requests.get(link)
    soup = BeautifulSoup(req.text, "html.parser")
    header = soup.find('title').text
    if '.wikia.' in link:
        return header.split(' | ')[0]
    else:
        return header.split(' — ')[0]


def wikia_links(wiki, header):
    '''Generator of titles of linked articles to given one on wiki'''
    page = wikia.page(wiki, header)
    soup = BeautifulSoup(page.html(), "html.parser")
    for paragraph in soup.find_all('p'):
        for link in paragraph.find_all('a'):
            try:
                yield link['title']
            except KeyError:
                continue


class Article:
    '''Class, containing current header, wiki and language'''
    wiki = 'wikipedia'
    lang = 'ru'

    def __init__(self, input_str):
        url = input_str.split('/')
        if 'http' in url[0]:
            # Dealing with given link
            self.wiki, self.lang = get_lang_wiki(url)
            self.header = get_article_name(input_str)
        else:
            # Otherwise - got <wikia_name>.wikia/(wikipedia) <article_name>
            input_list = input_str.split()
            if 'wiki' in input_list[0]:
                if 'wikia' in input_list[0]:
                    self.wiki = input_list[0].split('.')[0]
                self.header = ' '.join(input_list[1:])
            else:
                self.header = input_str
        wikipedia.set_lang(self.lang)
        wikia.set_lang(self.lang)
        # assigning generator if dealing with wikia page
        if self.wiki != 'wikipedia':
            self.links = wikia_links(self.wiki, self.header)

    def get_page(self):
        '''Returns page on wikipedia or wikia'''
        if self.wiki == 'wikipedia':
            try:
                page = wikipedia.page(self.header)
                self.links = page.links
                return page
            except wikipedia.exceptions.PageError:
                raise PageNotFound(self.wiki, self.header)
        else:
            try:
                return wikia.page(self.wiki, self.header)
            except wikia.wikia.WikiaError:
                raise PageNotFound(self.wiki, self.header)

    def linked_articles(self, max_depth, **kwargs):
        '''Generator of articles' headers linked with current'''
        try:
            page = self.get_page()
        except PageNotFound as e:
            # If it is not recursive - there is no such page
            if len(kwargs) == 0:
                raise e
            # otherwise - link to non-existing page
            else:
                return
        except wikipedia.exceptions.DisambiguationError as e:
            if len(kwargs) == 0:
                raise e
            else:
                return
        yield self.header, page.content
        if max_depth > 1:
            for header in self.links:
                article = Article('{}.wikia {}'.format(self.wiki, header))
                yield from article.linked_articles(max_depth - 1,
                                                   recursive=True)


class TrainRequest:
    '''Contains request + depth'''
    def __init__(self, input_str):
        r = input_str.split()
        self.max_depth = 1
        try:
            self.max_depth = int(r[-1])
            self.article = Article(' '.join(r[:-1]))
        except ValueError:
            self.article = Article(input_str)
