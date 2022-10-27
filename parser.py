from sqlalchemy.orm import mapper, Session
from sqlalchemy import create_engine, MetaData, Table
from time import sleep, mktime, time
from bs4 import BeautifulSoup as bs
from random import shuffle, random
from urllib.request import urljoin
from datetime import datetime
from os import path
import dateparser
import requests
import pdb

from models import Resource, Items

engine = create_engine("sqlite:///db.sqlite", echo=False)
meta = MetaData(engine)

resource = Table('resource', meta, autoload=True)
items = Table('items', meta, autoload=True)

mapper(Resource, resource)
mapper(Items, items)


class Parser:
    def __init__(self,
                RESOURCE_NAME,
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
        self.RESOURCE_NAME = RESOURCE_NAME
        self.top_tag = top_tag
        self.bottom_tag = bottom_tag
        self.title_cut = title_cut
        self.date_cut = date_cut
        self.current_page = current_page
        self.is_ended = False
        self.news_url = []
        self.parsed_row = dict()

    def read_last_page(self):
        path_to_file = path.join("last_pages", self.RESOURCE_NAME)
        with open(path_to_file) as file:
            last_page = int(file.readline().strip())  
            self.current_page = last_page
            return last_page

    def get_full_url(self, href) -> dict:
        return urljoin(self.RESOURCE_URL+'/', str(href))

    def get_news_links(self) -> list:

        last_page_number = self.read_last_page()

        if self.is_ended:
            raise requests.exceptions.BaseHTTPError()

        page_of_all_news_link = self.get_full_url(last_page_number + 1)
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

            self.write_last_page(last_page_number + 1)
            return full_links

        except requests.exceptions.BaseHTTPError() as e:
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
            row['nd_date'] = mktime(date_obj.timetuple())

            row['s_date'] = int(time())

            row['not_date'] = date_obj.strftime("%Y-%m-%d")
            self.parsed_row = row

            return row

        except requests.ConnectionError:
            random_time = random() * 10 + 2
            sleep(random_time)

        


    def parse_all_rows_of_current_page(self) -> list:
        last_page_number = self.read_last_page()
        news_links = self.get_news_links()
        rows = []
        for link in news_links:
            try:
                row = self.parse_row(link)
                rows.append(row)
            except requests.exceptions.ConnectionError as err:
                continue
            except AttributeError:
                continue

        return rows


    def write_last_page(self, page_number):
        """Здесь я сохраню номер последней страницы с данными.
        В случае сбоя можно будет продолжить с нее"""
        path_to_file = path.join("last_pages", self.RESOURCE_NAME)
        with open( path_to_file, 'w') as f:
            f.write(str(page_number))


    def save_rows(self, rows):
        with Session(engine) as session:
            session.begin()
            for row in rows:
                item = Items(**row)
                session.add(item)
                
            session.commit()
    

if __name__ == "__main__":
    with Session(engine) as session:
        resources = [res.__dict__ for res in session.query(Resource).all()]
    parsers = [Parser(**re) for re in resources]
    while parsers:
        filter(lambda parser: not parser.is_ended, parsers)
        for parser in parsers:
            rows = parser.parse_all_rows_of_current_page()
            parser.save_rows(rows)
