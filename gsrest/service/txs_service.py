from cassandra.query import SimpleStatement

from gsrest.db.cassandra import get_session
from gsrest.model.txs import Tx
from gsrest.service.rates_service import get_rates, list_rates

TXS_PAGE_SIZE = 100
TX_PREFIX_LENGTH = 5


def get_tx(currency, tx_hash):
    session = get_session(currency, 'raw')

    query = "SELECT * FROM transaction WHERE tx_prefix = %s AND tx_hash = %s"
    result = session.execute(query, [tx_hash[:TX_PREFIX_LENGTH],
                                     bytearray.fromhex(tx_hash)])
    if result:
        return Tx.from_row(result[0],
                           get_rates(currency,
                                     result[0].height)['rates']).to_dict()
    return None


def list_txs(currency, paging_state=None):
    session = get_session(currency, 'raw')

    query = "SELECT * FROM transaction"
    statement = SimpleStatement(query, fetch_size=TXS_PAGE_SIZE)
    results = session.execute(statement, paging_state=paging_state)

    paging_state = results.paging_state
    heights = [row.height for row in results.current_rows]
    rates = list_rates(currency, heights)
    tx_list = [Tx.from_row(row, rates[row.height])
               .to_dict() for row in results.current_rows]

    return paging_state, tx_list


def list_matching_txs(currency, expression, leading_zeros):
    session = get_session(currency, 'raw')
    query = 'SELECT tx_hash from transaction where tx_prefix = %s'
    results = session.execute(query, [expression[:TX_PREFIX_LENGTH]])
    txs = ["0" * leading_zeros + str(hex(int.from_bytes(row.tx_hash,
                                                        byteorder="big")))[2:]
           for row in results]
    return [tx for tx in txs if tx.startswith(expression)]
