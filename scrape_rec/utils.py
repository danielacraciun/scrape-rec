import os
import uuid
import pickle

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base  


POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'chungus'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 5435
POSTGRES_DB = 'realestate'


db_string = 'postgres://{user}:{password}@{host}:{port}/{db}'.format(
  user=POSTGRES_USER,
  password=POSTGRES_PASSWORD,
  host=POSTGRES_HOST,
  port=POSTGRES_PORT,
  db=POSTGRES_DB
)

db = sa.create_engine(db_string)
base = declarative_base()


class RealestateApartment(base):   
    __tablename__ = POSTGRES_DB 

    fingerprint = sa.Column(sa.String, primary_key=True) 

    # Mandatory
    title = sa.Column(sa.String, nullable=False) 
    description = sa.Column(sa.String, nullable=False)
    posted_date = sa.Column(sa.DateTime, nullable=False)
    price = sa.Column(sa.Integer, nullable=False)
    currency = sa.Column(sa.String, nullable=False)

    # Nullable
    partitioning = sa.Column(sa.String)
    surface = sa.Column(sa.Integer)
    building_year = sa.Column(sa.String)
    floor = sa.Column(sa.Integer)
    number_of_rooms = sa.Column(sa.Integer)
    terrace = sa.Column(sa.Boolean)
    parking = sa.Column(sa.Boolean)
    cellar = sa.Column(sa.Boolean)
    source_website = sa.Column(sa.String)
    source_offer = sa.Column(sa.String)
    neighborhood = sa.Column(sa.String)
    link = sa.Column(sa.String)


def get_postgres_session():
    # To fix db table changes errors enable once
    # db.execute('DROP TABLE realestate;')
    base.metadata.create_all(db)
    Session = sa.orm.sessionmaker(db)  
    return Session()


def get_metadata(rpath):
    with open(os.path.join(rpath, 'pickled_meta'), 'rb') as f: 
        return pickle.load(f) 

def get_response_from_cache_by_id(rpath):
    metadata = get_metadata(rpath)

    with open(os.path.join(rpath, 'response_body'), 'rb') as f: 
        body = f.read() 
     
    with open(os.path.join(rpath, 'response_headers'), 'rb') as f: 
        rawheaders = f.read() 
 
    url = metadata.get('response_url') 
    status = metadata['status'] 
    headers = Headers(headers_raw_to_dict(rawheaders)) 
    respcls = responsetypes.from_args(headers=headers, url=url) 
    response = respcls(url=url, headers=headers, status=status, body=body) 
 
    return response 


HTTPCACHE_DIR = '/var/lib/httpcache/'

def get_all_responses_from_cache(spider):
    root_dir = os.path.join(HTTPCACHE_DIR, spider.name)
    for current_root, directories, files in os.walk(root_dir): 
        if files and not directories: 
            yield get_response_from_cache_by_id(current_root) 


def get_all_urls_from_httpcache(spider_name):
    root_dir = os.path.join(HTTPCACHE_DIR, spider_name)
    for current_root, directories, files in os.walk(root_dir): 
        if files and not directories: 
            meta = get_metadata(current_root)
            yield meta.get('url')
