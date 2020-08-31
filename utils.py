from typing import Dict
import requests
from os.path import join
from pathlib import Path
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from retry import retry
from consts import HTML_PARSER, DOWNLOAD_PICTURE_PATH, ANIMAL_NAME, PICTURE_URL


@retry(Exception, delay=1, backoff=2, max_delay=4)
def get_html_page_by_url(url: str) -> BeautifulSoup:
    """
    :param url:
    :return: html page
    """
    html_page = requests.get(url).text
    return BeautifulSoup(html_page, HTML_PARSER)


@retry(Exception, delay=1, backoff=2, max_delay=4)
def download_image(url: str, animal_name: str) -> str:
    """
    :param url:
    :param animal_name:
    :return: animal picture path
    """
    if url:
        print("downloading image of: {}".format(animal_name))
        picture_path = join(DOWNLOAD_PICTURE_PATH, f"{animal_name}.{url.split('.')[-1]}")
        Path(DOWNLOAD_PICTURE_PATH).mkdir(parents=True, exist_ok=True)
        urlretrieve(url, picture_path)
    else:
        picture_path = "there is no picture for this animal"
    return picture_path


def print_dictionary(animals_by_collateral_adjective: Dict) -> None:
    """
    Prints the dictionary as follows:

    collateral_adjective_1
	    animal_name_1 animal_picture_path
    collateral_adjective_2
	    animal_name_2 animal_picture_path
	    animal_name_3 animal_picture_path
	    animal_name_4 animal_picture_path

    :param animals_by_collateral_adjective:
    """

    for adjective, animals in animals_by_collateral_adjective.items():
        print(adjective)
        for animal in animals:
            print('\t', animal[ANIMAL_NAME], animal[PICTURE_URL])
