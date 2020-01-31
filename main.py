#!flask/bin/python
from flask import Flask
import endpoints

def main():
    # instantiate node
    app = Flask(__name__)
    endpoints.endpoints(app)
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()