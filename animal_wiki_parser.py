import re
from consts import HtmlTags, AnimalWikiPageConsts, PICTURE_URL, ANIMAL_NAME
from utils import get_html_page_by_url, download_image


def parse_row(row, lock, animals_by_collateral_adjective):
    """
    For each row in the table extracts parameters such as animal's name, image and collateral adjective
    updates the dictionary as follows:

    {collateral_adjective_1 :{animal_name_1: animal_picture_path_1},{animal_name_2: animal_picture_path_2}}},
    {collateral_adjective_2 :{animal_name_3: animal_picture_path_3}}

    :param row:
    :param lock:
    :param animals_by_collateral_adjective:
    :return:
    """
    link_tag = row.find(HtmlTags.A)
    if link_tag:
        animal_picture_dict = create_animal_picture_dict(link_tag)
        table_fields = row.find_all(HtmlTags.TD)
        if len(table_fields) > AnimalWikiPageConsts.COLLATERAL_ADJECTIVE_INDEX:
            collateral_adjective_list = get_collateral_adjective(table_fields)
            for adjective in collateral_adjective_list:
                update_results(adjective, animal_picture_dict, lock, animals_by_collateral_adjective)


def create_animal_picture_dict(tag):
    """
    extract from tag animal name and animal picture and update dictionary
    """
    animal_name = tag.get(HtmlTags.TITLE)
    animal_image_path = download_image(get_specific_animal_url(tag), animal_name)
    return {ANIMAL_NAME: animal_name, PICTURE_URL: animal_image_path}


def get_specific_animal_url(animal_link_tag):
    """
    :param animal_link_tag:
    :return: url for animal picture
    """
    url_for_animal = AnimalWikiPageConsts.HEAD_HTML + str(animal_link_tag.get(HtmlTags.HREF))
    html_page_for_animal = get_html_page_by_url(url_for_animal)
    return extract_picture_url(html_page_for_animal)


def extract_picture_url(html_page):
    """
    :param html_page:
    :return: animal picture url
    """
    metas = html_page.findAll(HtmlTags.META)
    for meta in metas:
        if meta.attrs.get(HtmlTags.PROPERTY) == AnimalWikiPageConsts.IMAGE_PROPERTY:
            return meta[HtmlTags.CONTENT]


def get_collateral_adjective(fields):
    """
    :param fields:
    :return: collateral_adjective
    """
    collateral_adjectives_text = fields[AnimalWikiPageConsts.COLLATERAL_ADJECTIVE_INDEX].text
    collateral_adjective_cleaned = re.sub('\[(.*?)\] | \((.*?)\)', '', collateral_adjectives_text)
    return collateral_adjective_cleaned.split(" ")


def update_results(adjective, animal_picture_dict, lock, animals_by_collateral_adjective):
    """
    Updates the dictionary with the new data.
    If the key(adjective) already exists - we will add the new value(animal_picture_dict) to it,
    and if not we will add a new key
    :param adjective:
    :param animal_picture_dict:
    :param lock:
    :param animals_by_collateral_adjective:
    """
    with lock:
        if adjective in animals_by_collateral_adjective:
            animals_by_collateral_adjective[adjective].append(animal_picture_dict)
        else:
            animals_by_collateral_adjective[adjective] = [animal_picture_dict]
