from threading import Thread, Lock
from typing import List
from bs4.element import Tag
from utils import get_html_page_by_url, print_dictionary
from animal_wiki_parser import parse_row
from consts import AnimalWikiPageConsts, HtmlTags


def calculate_rows_concurrently(table_rows: List[Tag]) -> None:
    row_tasks = []
    for row in table_rows:
        row_task = Thread(target=parse_row, args=(row, lock, animals_by_collateral_adjective,))
        row_task.start()
        row_tasks.append(row_task)
    for task in row_tasks:
        task.join()


if __name__ == '__main__':
    animals_by_collateral_adjective = {}
    lock = Lock()
    html_response = get_html_page_by_url(AnimalWikiPageConsts.URL)
    # NOTE: extract animals table (the second table)
    table = html_response.findAll(HtmlTags.TABLE, attrs={HtmlTags.CLASS: AnimalWikiPageConsts.TABLE_CLASS})[1]
    # NOTE: ignore the first row that represent the column title
    table_rows = table.find_all(HtmlTags.TR)[1:]
    calculate_rows_concurrently(table_rows)
    print_dictionary(animals_by_collateral_adjective)
