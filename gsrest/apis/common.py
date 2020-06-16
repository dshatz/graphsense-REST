from flask_restplus import Namespace, fields

from gsrest.util.checks import MAX_DEPTH

DEFAULT_DEPTH = 1
DEFAULT_BREADTH = 16

api = Namespace('common',
                path='/common',
                description='Common models and definitions')

"""
REST interface argument parsers
"""

page_parser = api.parser()
page_parser.add_argument("page", location="args",
                         help="Resumption token for retrieving the next page")

label_parser = api.parser()
label_parser.add_argument("currency", location="args")
label_parser.add_argument("label", required=True, location="args",
                          help="The label of an entity")

search_parser = api.parser()
search_parser.add_argument("currency", location="args",
                           help="Cryptocurrency")
search_parser.add_argument("q", location="args", required=True,
                           help="It can be (the beginning of) an address,"
                                " a transaction or a label")
search_parser.add_argument("limit", type=int, location="args",
                           help="Maximum number of search results")

page_size_parser = page_parser.copy()
page_size_parser.add_argument("pagesize", type=int, location="args",
                              help="Number of items returned in a single page")

neighbors_parser = page_size_parser.copy()
neighbors_parser.add_argument("direction", required=True, location="args",
                              choices=('in', 'out'),
                              help="Incoming or outgoing neighbors")
neighbors_parser.add_argument("targets", required=False, location="args",
                              help="Restrict result to the given set of "
                                   "comma separated ids")

links_parser = api.parser()
links_parser.add_argument("neighbor", required=True, location="args",
                          help="Outgoing neighbor receiving funds")

search_neighbors_parser = api.parser()
search_neighbors_parser.add_argument("direction", location="args")
search_neighbors_parser.add_argument("category", location="args")
search_neighbors_parser.add_argument("addresses", location="args")
search_neighbors_parser.add_argument("depth", type=int, default=DEFAULT_DEPTH,
                                     location="args")
search_neighbors_parser.add_argument("breadth", type=int,
                                     default=DEFAULT_BREADTH, location="args")
search_neighbors_parser.add_argument("skipNumAddresses", type=int,
                                     default=DEFAULT_BREADTH, location="args")
search_neighbors_parser.add_argument("field", location="args")
search_neighbors_parser.add_argument("min", type=int, default=0,
                                     location="args")
search_neighbors_parser.add_argument("max", type=int, location="args")
search_neighbors_parser.add_argument("fieldcurrency", location="args")


"""
Type definitions reused across interfaces
"""

value_model = {
    "eur": fields.Float(required=True, description="EUR value"),
    "value": fields.Integer(required=True, description="Value"),
    "usd": fields.Float(required=True, description="USD value")
}
value_response = api.model("value_response", value_model)

rates_model = {
    "eur": fields.Float(required=True, description="EUR/crypto rate"),
    "usd": fields.Float(required=True, description="USD/crypto rate")
}
rates_response = api.model("rates_response", rates_model)

height_rates_model = {
    "height": fields.Integer(required=True, description="Block height"),
    "rates": fields.Nested(rates_response, required=True, description="Rates")
}
height_rates_response = api.model("height_rates_response", height_rates_model)

tag_model = {
    "label": fields.String(required=True, description="Label"),
    "address": fields.String(required=True, description="Address"),
    "source": fields.String(required=True, description="Source"),
    "tagpack_uri": fields.String(required=True, description="Tagpack URI"),
    "currency": fields.String(required=True, description="Currency"),
    "lastmod": fields.Integer(required=True, description="Last modified"),
    "active": fields.Boolean(required=True, description="Active address"),
    "category": fields.String(required=False, description="Category"),
    "abuse": fields.String(required=False, description="Abuse")
}
tag_response = api.model("tag_response", tag_model)


tx_summary_model = {
    "height": fields.Integer(required=True, description="Transaction height"),
    "timestamp": fields.Integer(required=True,
                                description="Transaction timestamp"),
    "tx_hash": fields.String(required=True, description="Transaction hash")
}
tx_summary_response = api.model("tx_summary_response", tx_summary_model)

block_model = {
    "block_hash": fields.String(required=True, description="Block hash"),
    "height": fields.Integer(required=True, description="Block height"),
    "no_txs": fields.Integer(
        required=True, description="Number of transactions"),
    "timestamp": fields.Integer(
        required=True, description="Transaction timestamp"),
}
block_response = api.model("block_response", block_model)

block_list_model = {
    "blocks": fields.List(fields.Nested(block_response),
                          required=True, description="Block list"),
    "next_page": fields.String(required=True, description="The next page")
}
block_list_response = api.model("block_list_response", block_list_model)

block_tx_model = {
    "tx_hash": fields.String(required=True, description="Transaction hash"),
    "no_inputs": fields.Integer(
        required=True, description="Number of inputs"),
    "no_outputs": fields.Integer(
        required=True, description="Number of outputs"),
    "total_input": fields.Nested(
        value_response, required=True, description="Total input value"),
    "total_output": fields.Nested(
        value_response, required=True, description="Total output value")
}
block_tx_response = api.model("block_tx_response", block_tx_model)

block_txs_model = {
    "height": fields.Integer(required=True, description="Block height"),
    "txs": fields.List(fields.Nested(
        block_tx_response), required=True, description="Block list")
}
block_txs_response = api.model("block_txs_response", block_txs_model)

address_model = {
    "address": fields.String(required=True, description="Address"),
    "balance": fields.Nested(value_response, required=True,
                             description="Balance"),
    "first_tx": fields.Nested(tx_summary_response, required=True,
                              description="First transaction"),
    "last_tx": fields.Nested(tx_summary_response, required=True,
                             description="Last transaction"),
    "in_degree": fields.Integer(required=True, description="In-degree value"),
    "out_degree": fields.Integer(required=True,
                                 description="Out-degree value"),
    "no_incoming_txs": fields.Integer(required=True,
                                      description="Incoming transactions"),
    "no_outgoing_txs": fields.Integer(required=True,
                                      description="Outgoing transactions"),
    "total_received": fields.Nested(value_response, required=True,
                                    description="Total received"),
    "total_spent": fields.Nested(value_response, required=True,
                                 description="Total spent"),
}
address_response = api.model("address_response", address_model)

address_tx_model = {
    "address": fields.String(required=True, description="Address"),
    "height": fields.Integer(required=True, description="Transaction height"),
    "timestamp": fields.Integer(required=True,
                                description="Transaction timestamp"),
    "tx_hash": fields.String(required=True, description="Transaction hash"),
    "value": fields.Nested(value_response, required=True)
}
address_tx_response = api.model("address_tx_response", address_tx_model)

address_txs_model = {
    "next_page": fields.String(required=True, description="The next page"),
    "address_txs": fields.List(fields.Nested(address_tx_response),
                               required=True,
                               description="The list of transactions")
}
address_txs_response = api.model("address_txs_response", address_txs_model)

address_tags_model = address_model.copy()
address_tags_model["tags"] = fields.List(fields.Nested(tag_response,
                                                       required=True))
address_tags_response = api.model("address_tags_response",
                                  address_tags_model)

entity_model = {
    "balance": fields.Nested(value_response, required=True,
                             description="Balance"),
    "entity": fields.Integer(required=True, description="Entity id"),
    "first_tx": fields.Nested(tx_summary_response, required=True),
    "last_tx": fields.Nested(tx_summary_response, required=True),
    "no_addresses": fields.Integer(required=True,
                                   description="Number of addresses"),
    "in_degree": fields.Integer(required=True, description="In-degree value"),
    "out_degree": fields.Integer(required=True,
                                 description="Out-degree value"),
    "no_incoming_txs": fields.Integer(required=True,
                                      description="Incoming transactions"),
    "no_outgoing_txs": fields.Integer(required=True,
                                      description="Outgoing transactions"),
    "total_received": fields.Nested(value_response, required=True),
    "total_spent": fields.Nested(value_response, required=True),
    "tag_coherence": fields.Float(required=False, description="Tag coherence"),
}

entity_tags_model = entity_model.copy()
entity_tags_model["tags"] = fields.List(fields.Nested(tag_response,
                                                      required=True))
entity_tags_response = api.model("entity_tags_response", entity_tags_model)

neighbor_model = {
    "id": fields.String(required=True, description="Node Id"),
    "node_type": fields.String(required=True, description="Node type"),
    "labels": fields.List(fields.String, required=True, description="Labels"),
    "balance": fields.Nested(value_response, required=True,
                             description="Balance"),
    "received": fields.Nested(value_response, required=True,
                              description="Received amount"),
    "no_txs": fields.Integer(required=True,
                             description="Number of transactions"),
    "estimated_value": fields.Nested(value_response, required=True)
}
neighbor_response = api.model("neighbor_response", neighbor_model)

neighbors_model = {
    "next_page": fields.String(required=True, description="The next page"),
    "neighbors": fields.List(fields.Nested(neighbor_response), required=True,
                             description="The list of neighbors")
}
neighbors_response = api.model("neighbors_response", neighbors_model)

link_model = {
    "tx_hash": fields.String(required=True, description="Transaction hash"),
    "height": fields.String(required=True, description="Block height"),
    "timestamp": fields.Integer(required=True,
                                description="Transaction timestamp"),
    "input_value": fields.Nested(value_response, required=True),
    "output_value": fields.Nested(value_response, required=True)
}
link_response = api.model("link_response", link_model)

links_model = {
    "links": fields.List(fields.Nested(link_response), required=True,
                         description="A limited list of transactions between "
                                     "two addresses")
}
links_response = api.model("links_response", links_model)

entity_address_model = address_model.copy()
entity_address_model['entity'] = fields.Integer(required=True,
                                                description="Entity id")

entity_address_response = api.model("entity_address_response",
                                    entity_address_model)

entity_addresses_model = {
    "next_page": fields.String(required=True, description="The next page"),
    "addresses": fields.List(fields.Nested(entity_address_response),
                             required=True,
                             description="The list of entity addresses")
}
entity_addresses_response = api.model("entity_addresses_response",
                                      entity_addresses_model)

input_output_model = {
    "address": fields.String(required=True, description="Address"),
    "value": fields.Nested(value_response, required=True,
                           description="Input/Output value")
}
input_output_response = api.model("input_output_response", input_output_model)

tx_model = {
    "tx_hash": fields.String(required=True, description="Transaction hash"),
    "coinbase": fields.Boolean(required=True,
                               description="Coinbase transaction flag"),
    "height": fields.Integer(required=True, description="Transaction height"),
    "inputs": fields.List(fields.Nested(input_output_response), required=True,
                          description="Transaction inputs"),
    "outputs": fields.List(fields.Nested(input_output_response), required=True,
                           description="Transaction inputs"),
    "timestamp": fields.Integer(required=True,
                                description="Transaction timestamp"),
    "total_input": fields.Nested(value_response, required=True),
    "total_output": fields.Nested(value_response, required=True),
}
tx_response = api.model("tx_response", tx_model)

tx_list_model = {
    "txs": fields.List(fields.Nested(tx_response),
                       required=True, description="Transaction list"),
    "next_page": fields.String(required=True, description="The next page")
}
tx_list_response = api.model("tx_list_response", tx_list_model)

concept_model = {
    "label": fields.String(required=True, description="Label"),
    "taxonomy": fields.String(required=True, description="Taxonomy"),
    "uri": fields.String(required=True, description="URI"),
    "description": fields.String(required=True, description="Description"),
    "id": fields.String(required=True, description="Id")
}
concept_response = api.model("concept_response", concept_model)

taxonomy_model = {
    "taxonomy": fields.String(required=True, description="Taxonomy"),
    "uri": fields.String(required=True, description="URI"),
}
taxonomy_response = api.model("taxonomy_response", taxonomy_model)


def search_neighbors_recursive(depth=7):
    mapping = {
        "node": fields.Nested(entity_tags_response, required=True,
                              description="Node"),
        "matching_addresses":
            fields.List(fields.Nested(address_tags_response,
                                      required=True,
                                      description="Addresses contained in "
                                                  "entity node that matched "
                                                  "the search query")),
        "relation": fields.Nested(neighbor_response,
                                  required=True,
                                  description="Relation to parent node")
    }
    if depth:
        mapping["paths"] = fields.List(fields.Nested(
            search_neighbors_recursive(depth - 1), required=True))
    return api.model("mapping{}".format(depth), mapping)


search_neighbors_model = {
    "paths": fields.List(fields.Nested(
        search_neighbors_recursive(MAX_DEPTH), required=True))}
search_neighbors_response = api.model("search_neighbors_response_depth_" +
                                      str(MAX_DEPTH), search_neighbors_model)


currency_search_model = {
    "addresses": fields.List(fields.String, required=True,
                             description="The list of found addresses"),
    "txs": fields.List(fields.String, required=True,
                       description="The list of found transactions"),
    "currency": fields.String(required=True, description="The cryptocurrency")
}
currency_search_response = api.model('currency_search_response',
                                     currency_search_model)

search_model = {
    'currencies': fields.List(fields.Nested(currency_search_response),
                              required=True,
                              description='List of matching addresses and '
                                          'transactions for a cryptocurrency'),
    'labels': fields.List(fields.String, required=True,
                          description="The list of matching labels"),
}
search_response = api.model("search_response", search_model)
