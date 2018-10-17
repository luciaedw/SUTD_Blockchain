from binascii import hexlify
import random
from ecdsa import SigningKey
from transaction import Transaction
from merkleTree import merkleTree
from blockChain import blockChain
from uuid import uuid4
from flask import Flask, jsonify, request
from miner import Miner


app = Flask(__name__)

testChain = blockChain()

miners = []
for i in range(5):
  sk = SigningKey.generate()  # uses NIST192p
  vk = sk.get_verifying_key().to_string()
  newMiner = Miner(sk, hexlify(vk).decode(), testChain)
  miners.append(newMiner)

@app.route('/transaction/new', methods=['POST'])
def newTransaction():
    values = request.get_json()

    transaction = miners[0].createTransaction(
        miners[values['receiver']].pubKey, values['amount'],  values['comment'])

    miners[1].addTransaction(transaction)
    miners[1].mine()
    miners[0].validateNewBlock(miners[1].endBlock)
    miners[0].updateEndBlock()

    response = {
        'endBlock': str(miners[0].endBlock),
    }
    return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine():
  # Mine first block, give it to miner 1 to validate
  miners[0].mine()
  miners[1].validateNewBlock(miners[0].endBlock)
  miners[1].updateEndBlock()

  response = {
      'endBlock': str(miners[0].endBlock),
  }
  return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def fullChain():
    response = {
        'blocks': str(testChain.blocks),
    }
    return jsonify(response), 200


@app.route('/miners/<int:miner_id>')
def banace(miner_id):
    response = {
        'Miner': miner_id,
        'Balance': str(miners[miner_id].balance),
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
