from sqlalchemy import MetaData, Table, Column, Integer, String, Text, Date, ForeignKey, create_engine
from sqlalchemy.orm import mapper, Session
from bs4 import BeautifulSoup as bs
from models import Resource, Items
import requests
import pdb
from urllib.request import urljoin
from random import shuffle, random
from time import sleep
import dateparser
from time import mktime, time

engine = create_engine("sqlite:///db.sqlite", echo=False)
meta = MetaData(engine)

resource = Table('resource', meta, autoload=True)
items = Table('items', meta, autoload=True)

mapper(Resource, resource)
mapper(Items, items)

# dbsession = sessionmaker(bind=engine)
# session = dbsession()

class Parser:
    def __init__(self,
                RESOURCE_ID,
                RESOURCE_URL,
                top_tag,
                bottom_tag,
                title_cut,
                date_cut,
                current_page = 1,
                *args,
                **kwargs
                ):
        self.RESOURCE_ID = RESOURCE_ID
        self.RESOURCE_URL = RESOURCE_URL
        self.top_tag = top_tag
        self.bottom_tag = bottom_tag
        self.title_cut = title_cut
        self.date_cut = date_cut
        self.current_page = current_page
        self.is_ended = False
        self.news_url = []
        self.parsed_row = dict()

    def set_current_page(self):
        with open(self.RESOURCE_ID) as file:
            self.current_page = int(file.readline().strip())

    def get_full_url(self, href: str) -> dict:
        return urljoin(self.RESOURCE_URL+'/', str(href))

    def get_news_links_from_page_n(self, n: int) -> list:
        if self.is_ended:
            raise requests.exceptions.ConnectionError()

        self.current_page = n

        page_of_all_news_link = self.get_full_url(n)
        try:
            response = requests.get(page_of_all_news_link)

            if not page_of_all_news_link:
                self.is_ended = True
                return []
            
            bs_obj = bs(response.text, 'html.parser')
            first_news_tag = bs_obj.select_one(self.top_tag)
            news_tags = first_news_tag.find_next_siblings()
            hrefs = [tag.find('a', href=True).get('href') for tag in news_tags]
            full_links = [self.get_full_url(href) for href in hrefs]
            self.news_url = full_links
            shuffle(self.news_url)
            return full_links

        except requests.exceptions.ConnectionError() as e:
            return []


    def parse_row(self, url: str) -> dict:
        row = dict()
        try:
            response = requests.get(url)
            bsobj = bs(response.text, 'html.parser')
            row['res_id'] = self.RESOURCE_ID
            row['link'] = url
            row['title'] = bsobj.select_one(self.title_cut).text.strip()
            row['content'] = bsobj.select_one(self.bottom_tag).text.strip()

            date_str = bsobj.select_one(self.date_cut).get('datetime')
            date_obj = dateparser.parse(date_str)
            row['nd_date'] = int(mktime(date_obj.timetuple()))

            row['s_date'] = int(time())

            row['not_date'] = date_obj.strftime("%Y-%m-%d")
            self.parsed_row = row

            return row

        except requests.ConnectionError:
            random_time = random() * 10 + 2
            sleep(random_time)


    def parse_all_rows_of_page_n(self, n: int) -> list:
        news_links = self.get_news_links_from_page_n(n)
        shuffle(news_links)
        rows = []
        for link in news_links:
            try:
                row = self.parse_row(link)
                rows.append(row)

            except requests.exceptions.ConnectionError as err:
                continue
        return rows


def save_row(row):
    with Session(engine) as session:
        session.begin()
        session.add(Items(**row))
        session.commit()
    

def write_current_page_of_parser(parser_name_file, page_number):
    """Здесь я сохраню номер последней страницы с данными. В случае сбоя можно будет продолжить с нее"""
    with open(parser_name_file, 'w') as f:
        write(page_number)

        

if __name__ == "__main__":
    resources = [res.__dict__ for res in session.query(Resource).all()]
    parsers = [Parser(**re) for re in resources]
    page_number = 1
    while parsers:
        filter(lambda parser: not parser.is_ended, parser)
        for parser in parsers:
            rows = parser.parse_all_rows_of_page(page_number)
            save_row(row)
            pdb.set_trace()

        page_number += 1
