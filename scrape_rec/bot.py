import telegram

from scrape_rec.db_wrapper import RealestateApartment, get_postgres_session, UserSettings
from scrape_rec.settings import BOT_TOKEN

bot = telegram.Bot(token=BOT_TOKEN)
session = get_postgres_session()


def apply_filter(attr, attr_value, current_results, column):
    if attr.startswith('min'):
        return current_results.filter(column >= attr_value)
    elif attr.startswith('max'):
        return current_results.filter(column <= attr_value)
    return current_results


def build_message_text(rows):
    return ''.join(
        '🏡 {}\nPrice: {}{}{}{}{}\nLink: {}\n\n'.format(
            row.title, row.price,
            ' Surface: {}'.format(row.surface) if row.surface else '',
            ' Number of rooms: {}'.format(row.number_of_rooms) if row.number_of_rooms else '',
            ' Floor: {}'.format(row.floor) if row.floor else '',
            ' Neighborhood: {}'.format(row.neighborhood) if row.neighborhood is not 'not found' else '',
            row.link)
        for row in rows
    )


def get_results_for_user(options, since):
    latest_listings = session.query(RealestateApartment).filter(
        RealestateApartment.scraped_date >= since, RealestateApartment.currency == 'EUR')

    corresponding_columns = {
        'minprice': RealestateApartment.price,
        'maxprice': RealestateApartment.price,
        'minrooms': RealestateApartment.number_of_rooms,
        'maxrooms': RealestateApartment.number_of_rooms,
        'minsurface': RealestateApartment.surface,
        'maxsurface': RealestateApartment.surface,
        'minfloor': RealestateApartment.floor,
        'maxfloor': RealestateApartment.floor,
    }
    for attr in corresponding_columns.keys():
        if options.get(attr):
            latest_listings = apply_filter(attr, options[attr], latest_listings, corresponding_columns[attr])

    return build_message_text(latest_listings.all())


def send_message(to, listings):
    bot.send_message(chat_id=to, text=listings)


def send_listing_notifications(since):
    for user in session.query(UserSettings).all():
        msg = get_results_for_user(user.user_settings, since)
        if msg:
            send_message(user.chat_id, msg)
