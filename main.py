#!flask/bin/python
from flask import Flask
import os
from blockchain import Blockchain
import endpoints
# from multiprocessing import Pool

THREADS = os.cpu_count()
# data = ((1, 1000), (1001, 2000), (2001, 3000), (3001, 4000))

def main():
    # instantiate flask node
    app = Flask(__name__)
    # instantiate blockchain
    blockchain = Blockchain()

    endpoints.endpoints(app, blockchain)
    app.run(debug=True, host='0.0.0.0', port=5000)

# def np_worker():
#     print("worker processing")

# def np_handler():
#     pool = multiprocessing.Pool(THREADS)
#     pool.map(np_worker, data)

if __name__ == '__main__':
    print(THREADS)
    # np_handler()
    main()