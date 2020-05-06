from cassandra.query import SimpleStatement, dict_factory
from cassandra.concurrent import execute_concurrent
from flask import current_app

from gsrest.db.cassandra import (get_session, get_keyspace_mapping,
                                 get_supported_currencies)
from gsrest.model.rates import ExchangeRate
from gsrest.service.general_service import get_statistics


RATES_TABLE = 'exchange_rates'
CACHED_EXCHANGE_RATES = dict()
LAST_BLOCK_HEIGHT = dict()


def init_app(app):
    # do not load in development mode
    if not app.config.get('DUMMY_EXCHANGE_RATES'):
        app.before_first_request(load_all_rates)


def load_all_rates():
    """ Load and cache exchange rates for all known currencies """

    currencies = get_supported_currencies()
    for currency in currencies:
        CACHED_EXCHANGE_RATES[currency] = dict()
        LAST_BLOCK_HEIGHT[currency] = 0
        load_rates(currency)


def load_supported_fiat_currencies(currency):
    """ Load supported fiat currencies from rates table schema """

    current_app.logger.info("Querying supported fiat currencies")

    keyspace = get_keyspace_mapping(currency, 'transformed')
    session = get_session(currency, 'transformed')
    session.row_factory = dict_factory

    query = "SELECT column_name FROM system_schema.columns \
             WHERE keyspace_name = '{}' \
             AND table_name = '{}'".format(keyspace, RATES_TABLE)

    results = session.execute(query)
    currencies = []
    for row in results:
        if row['column_name'] != 'height':
            currencies.append(row['column_name'])
    return currencies


def load_rates(currency):
    """ Load and cache exchange rates for a given currency """

    current_app.logger.info("Loading all exchange rates for {}..."
                            .format(currency))

    supported_fiat_currencies = load_supported_fiat_currencies(currency)
    LAST_BLOCK_HEIGHT[currency] = get_statistics(currency)['no_blocks'] - 1
    session = get_session(currency, 'transformed')
    session.row_factory = dict_factory

    query = "SELECT * FROM {}".format(RATES_TABLE)
    statement = SimpleStatement(query, fetch_size=10000)
    counter = 0
    for row in session.execute(statement):
        rates = {}
        for fiat_currency in supported_fiat_currencies:
            rates[fiat_currency] = row[fiat_currency]
        height = row['height']
        CACHED_EXCHANGE_RATES[currency][height] = ExchangeRate(height,
                                                               rates)
        counter = counter + 1

    current_app.logger.info("Finished loading {} exchange rates for {}."
                            .format(counter, currency))


def get_rates(currency, height=-1):
    """ Returns the exchange rate for a given block height """

    # used in development mode only
    if current_app.config.get('DUMMY_EXCHANGE_RATES'):
        return ExchangeRate(height, {'eur': 0.5, 'usd': 0.5}).to_dict()

    currency_rates = CACHED_EXCHANGE_RATES.get(currency)
    if not currency_rates:
        raise ValueError("Cannot load exchange rates. Unknown currency: {}"
                         .format(currency))
    if height == -1:
        height = LAST_BLOCK_HEIGHT[currency]
    height_rates = currency_rates.get(height)
    if not height_rates:
        raise ValueError("Cannot find height {} in currency {}"
                         .format(height, currency))

    return height_rates.to_dict()


def list_rates(currency, heights=-1):
    """ Returns the exchange rates for a list of block heights """
    session = get_session(currency, 'transformed')

    if heights == -1:
        heights = [get_statistics(currency)['no_blocks'] - 1]

    concurrent_query = "SELECT * FROM exchange_rates WHERE height = %s"
    statements_and_params = []
    for h in heights:
        statements_and_params.append((concurrent_query, [h]))
    rates = execute_concurrent(session, statements_and_params,
                               raise_on_first_error=False)
    height_rates = dict() # key: height, value: {'eur': 0, 'usd':0}
    for (success, rate) in rates:
        if not success:
            pass
        else:
            d = rate.one()._asdict()
            height_rates[d['height']] = {k: v for k, v in d.items()
                                         if k != 'height'}
    return height_rates
