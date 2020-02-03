import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.new_block(proof = 100, previous_hash = 1) #genesis (first) block

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
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

    # ----------------------------------------------------
    # def proof_of_work(self, last_proof, lower_value, upper_value):
        # proof = lower_value
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            # if (proof >= upper_value):
            #     return -1
            proof += 1
        return proof

    # TODO 
    # EDIT VALID PROOF METHOD TO GENERALIZE FOR DIFFERENT CRYPTOCURRENCIES 
    # (number of zeros)
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
     # ----------------------------------------------------

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while len(chain) > current_index:
            block = chain[current_index]

            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")

            # verify hash of block
            if block['previous_hash'] != self.hash(last_block):
                return False
            # verify proof of work
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
        return True
    
    def resolve_conflicts(self):
        # Consensus Algorithm, resolves conflicts by defaulting to the longest chain

        neighbors = self.nodes
        new_chain = None
        # only looking at chains longer than the current chain
        max_length = len(self.chain)

        # verify all chains on the network
        for node in neighbors:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # replace chain if a longer valid chain is found
        if new_chain:
            self.chain = new_chain
            return True
        return False # else return false