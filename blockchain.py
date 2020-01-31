#!flask/bin/python
import hashlib
import json
from time import time
from flask import Flask, jsonify, request

class Blockchain(object):
    def __init__(self):
        self.chain = []
    
    def new_block(self):
        # not yet implemented
        return nil

    def new_transaction(self):
        # not yet implemented
        return nil

    def hash(self):
        # not yet implemented
        return nil


    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        # proof = 0
        # while self.valid_proof(last_proof, proof) is False:
        #     proof += 1

        # return proof
        return nil

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        # guess = f'{last_proof}{proof}'.encode()
        # guess_hash = hashlib.sha256(guess).hexdigest()
        # return guess_hash[:4] == "0000"
        return nil


# Instantiate node
app = Flask(__name__)
blockchain = Blockchain()

# TESTING ENDPOINT
@app.route('/')
def index():
    return "hello world"


@app.route('/mine', methods=['GET'])
def mine():
    response = {
        'mine' : "true",
        'endpoint' : "success",
    }
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def chain():
    response = {
        'chain' : "true",
        'endpoint' : "success",
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
