#!flask/bin/python
import hashlib
import json
from uuid import uuid4
from time import time
from flask import Flask, jsonify, request

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.new_block(proof = 100, previous_hash = 1) #genesis (first) block
    
    def new_block(self, proof, previous_hash = None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.transactions = [] # reset current list of transactions

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender':sender,
            'recipient':recipient,
            'amount':amount,
        }
        self.transactions.append(transaction)
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    # @TODO EDIT PROOF OF WORK AND VALID PROOF METHODS TO GENERALIZE FOR DIFFERENT CRYPTOCURRENCIES
    # ----------------------------------------------------
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
     # ----------------------------------------------------


# instantiate node
app = Flask(__name__)
# generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
# instantiate blockchain
blockchain = Blockchain()

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
