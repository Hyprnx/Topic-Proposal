import datetime
import hashlib
import json

class Node:
    def __init__(self, prev_hash, data, signer, index):
        self.block = {
            'index': index,
            'signer': str(signer),
            'timestamp': str(datetime.datetime.now()),
            'data': data,
            'previous_hash': prev_hash
        }

    def get_block_info(self):
        hash = self._hash()
        self.block["_id"] = hash
        return self.block

    def _hash(self):
        encoded_block = json.dumps(self.block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

class SimpleBlockchain:
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

    node = Node(prev_hash='0', data=customer, signer='Duc Anh', index=2)
    print('nodeblock with hash:',node.get_block())

    demo_block = {
        'index': 2,
        'signer': 'Duc Anh',
        'timestamp': str(datetime.datetime.now()),
        'data': customer,
        'previous_hash': '0'}

    encoded_block = json.dumps(demo_block, sort_keys=True).encode()
    print('demo:', demo_block)
    hash = hashlib.sha256(encoded_block).hexdigest()
    demo_block['block_hash'] = hash
    print('demoblock with hash:', demo_block)
