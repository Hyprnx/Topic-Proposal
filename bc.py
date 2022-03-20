import datetime
import hashlib
import json

class Node:
    def __init__(self, prev_hash, data, index):
        self.block = {
            'index': index,
            'timestamp': str(datetime.datetime.now()),
            'data': data,
            'previous_hash': prev_hash}

    def get_block(self):
        self.block["block_hash"] = self.hash()
        return self.block

    def hash(self):
        encoded_block = json.dumps(self.block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(data=1, previous_hash='0')

    def create_block(self, data, previous_hash):
        pass
        # self.chain.append(block)
        # return block

    def previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()

            if hash_operation[:5] != '00000':
                return False
            previous_block = block
            block_index += 1

        return True


if __name__ == '__main__':
    customer = {
        'id': '456789',
        'name': 'Nam',
        'phone_number': '0332460789',
    }

    node = Node('0', data=customer, index=2)
    print(node.hash())

    demo_block = {
        'index': 2,
        'timestamp': str(datetime.datetime.now()),
        'proof': customer,
        'previous_hash': '0'}

    encoded_block = json.dumps(demo_block, sort_keys=True).encode()
    print(hashlib.sha256(encoded_block).hexdigest())
    print(datetime.datetime.now())
