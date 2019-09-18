import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from scrape_rec.settings import POSTGRES_DB, POSTGRES_DB_STRING

db = sa.create_engine(POSTGRES_DB_STRING)
base = declarative_base()


class RealestateApartment(base):
    __tablename__ = POSTGRES_DB

    fingerprint = sa.Column(sa.String, primary_key=True)

    # Mandatory
    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    scraped_date = sa.Column(sa.DateTime, nullable=False)
    price = sa.Column(sa.Integer, nullable=False)
    currency = sa.Column(sa.String, nullable=False)

    # Nullable
    posted_date = sa.Column(sa.DateTime)
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


class UserSettings(base):
    __tablename__ = 'telegram_bot_user_settings'

    chat_id = sa.Column(sa.Integer, nullable=False, primary_key=True)
    user_settings = sa.Column(sa.String)


def get_postgres_session():
    # To fix db table changes errors enable once
    # db.execute('DROP TABLE realestate;')
    base.metadata.create_all(db)
    Session = sa.orm.sessionmaker(db)
    return Session()
