from flask_restplus import Namespace, fields

api = Namespace('common',
                path='/',
                description='Common models and definitions')

"""
REST interface argument parsers
"""

page_parser = api.parser()
page_parser.add_argument(
    "page", type="str", location="args",
    help="Resumption token for retrieving the next page")

tags_parser = api.parser()
tags_parser.add_argument("tags", location="args")

direction_parser = api.parser()
direction_parser.add_argument("direction", location="args")

page_size_parser = page_parser.copy()
page_size_parser.add_argument("pagesize", location="args")

neighbors_parser = page_size_parser.copy()
neighbors_parser.add_argument("direction", location="args")


"""
Type definitions reused across interfaces
"""

value_model = {
    "eur": fields.Float(required=True, description="EUR value"),
    "value": fields.Integer(required=True, description="Value"),
    "usd": fields.Float(required=True, description="USD value")
}
value_response = api.model("value_response", value_model)

tag_model = {
    "label": fields.String(required=True, description="Label"),
    "address": fields.String(required=True, description="Address"),
    "source": fields.String(required=True, description="Source"),
    "tagpack_uri": fields.String(required=True, description="Tagpack URI"),
    "currency": fields.String(required=True, description="Currency"),
    "lastmod": fields.Integer(required=True, description="Last modified"),
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
}
entity_response = api.model("entity_response", entity_model)

entity_tags_model = entity_model.copy()
entity_tags_model["tags"] = fields.List(fields.Nested(tag_response,
                                                      required=True))
entity_tags_response = api.model("entity_tags_response", entity_tags_model)

neighbor_model = {
    "id": fields.String(required=True, description="Node Id"),
    "node_type": fields.String(required=True, description="Node type"),
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

entity_address_model = address_model.copy()
entity_address_model['entity'] = fields.Integer(required=True,
                                                description="Entity id")

entity_address_response = api.model("entity_address_response",
                                    entity_address_model)

entity_addresses_model = {
    "next_page": fields.String(required=True, description="The next page"),
    "addresses": fields.List(fields.Nested(entity_address_response),
                             required=True,
                             description="The list of entity adresses")
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
