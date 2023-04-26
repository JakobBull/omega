from flask_classful import FlaskView, route
from flask import Flask, jsonify, request
from omega.node.BlockchainUtils import BlockchainUtils
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from omega.node.Node import Node

node = None


class NodeAPI(FlaskView):

    def __init__(self):
        self.app = Flask(__name__)

    def start(self, port):
        NodeAPI.register(self.app, route_base='/')
        self.app.run(host='localhost', port=port)

    def injectNode(self, injectedNode: "Node"):
        global node
        node = injectedNode

    @route('/info', methods=['GET'])
    def info(self):
        return 'This is a communiction interface to a nodes blockchain', 200

    @route('/blockchain', methods=['GET'])
    def blockchain(self):
        return node.blockchain.toJson(), 200
    
    @route('/accountModel', methods=['GET'])
    def accountModel(self):
        return node.blockchain.accountModel.toJson(), 200

    @route('/transactionPool', methods=['GET'])
    def transactionPool(self):
        transactions = {}
        for ctr, transaction in enumerate(node.transactionPool.transactions):
            transactions[ctr] = transaction.toJson()
        return jsonify(transactions), 200

    @route('/transaction', methods=['POST'])
    def transaction(self):
        values = request.get_json()
        if not 'transaction' in values:
            return 'Missing transaction value', 400
        transaction = BlockchainUtils.decode(values['transaction'])
        node.handleTransaction(transaction)
        response = {'message': 'Received transaction'}
        return jsonify(response), 201
    
    """@route('/api/verify', methods=['GET', 'POST'])
    def testfn():
        # GET request
        if request.method == 'GET':
            data = node.blocks[-1].blockCount
            return jsonify(), 200
        # POST request
        if request.method == 'POST':
            print(request.get_json())  # parse as JSON
            return 'Success', 200"""