import os
import tempfile


class HtmlTags(object):
    META = "meta"
    CONTENT = 'content'
    PROPERTY = 'property'
    TABLE = "table"
    CLASS = "class"
    A = 'a'
    TR = 'tr'
    TD = 'td'
    TITLE = 'title'
    HREF = 'href'


class AnimalWikiPageConsts(object):
    URL = "https://en.wikipedia.org/wiki/List_of_animal_names"
    HEAD_HTML = 'https://en.wikipedia.org'
    TABLE_CLASS = "wikitable sortable"
    IMAGE_PROPERTY = 'og:image'
    COLLATERAL_ADJECTIVE_INDEX = 5


HTML_PARSER = 'html.parser'
DOWNLOAD_PICTURE_PATH = os.path.join(tempfile.gettempdir(), "AnimalPictures")
ANIMAL_NAME = 'name'
PICTURE_URL = 'picture_url'
