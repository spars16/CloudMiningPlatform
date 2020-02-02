import json
from flask import jsonify, request
from uuid import uuid4

def endpoints(app, blockchain):
    # generate a globally unique address for this node
    node_identifier = str(uuid4()).replace('-', '')

    # testing endpoint
    @app.route('/')
    def index():
        return "success!"

    # allows to post a new transaction
    @app.route('/transactions/new', methods=['POST'])
    def new_transaction():
        values = request.get_json()

        # verify that all required fields are in POSTed data
        required = ['sender', 'recipient', 'amount']
        if not all(k in values for k in required):
            return 'missing one or more of the following required fields: [sender, recipient, amount]', 400

        # new transaction
        index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
        
        response = {
            'message' : f'transaction will be added to block {index}',
        }
        return jsonify(response), 201

    # mines a new block into the chain
    @app.route('/mine', methods=['GET'])
    def mine():
        # run PoW algorithm and get next proof
        last_block = blockchain.last_block
        last_proof = last_block['proof']
        proof = blockchain.proof_of_work(last_proof)

        # recieve reward for mining
        blockchain.new_transaction(
            sender = "0", # sender is 0 to indicate this node has mined a new coin
            recipient = node_identifier,
            amount = 1,
        )

        # new block gets added to the chain
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)

        response = {
            'message': "new block forged!",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return jsonify(response), 200


    # prints the current full chain in json
    @app.route('/chain', methods=['GET'])
    def full_chain():
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }
        return jsonify(response), 200


    @app.route('/nodes/register', methods=['POST'])
    def register_nodes():
        values = request.get_json()

        nodes = values.get('nodes')
        if nodes is None:
            return "invalid list of nodes", 400

        for node in nodes:
            blockchain.register_node(node)

        response = {
            'message': 'new node added',
            'total_nodes': list(blockchain.nodes),
        }
        return jsonify(response), 201


    @app.route('/nodes/resolve', methods=['GET'])
    def consensus():
        replaced = blockchain.resolve_conflicts()

        if replaced:
            response = {
                'message': 'chain was replaced',
                'new_chain': blockchain.chain
            }
        else:
            response = {
                'message': 'current chain is authoritative',
                'chain': blockchain.chain
            }

        return jsonify(response), 200
