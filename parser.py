from sqlalchemy import MetaData, Table, Column, Integer, String, Text, Date, ForeignKey, create_engine
from sqlalchemy.orm import mapper, sessionmaker
from bs4 import BeautifulSoup as bs
from models import Resource, Items
import requests

engine = create_engine("sqlite:///db.sqlite", echo=False)
meta = MetaData(engine)

resource = Table('resource', meta, autoload=True)
items = Table('items', meta, autoload=True)

mapper(Resource, resource)
mapper(Items, items)

dbsession = sessionmaker(bind=engine)
session = dbsession()

class Parser(Resource):
    def __init__(self):
        super().__init__()

parser = Parser()

