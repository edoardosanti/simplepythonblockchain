#eedoardosanti(IG)

import hashlib
from time import time
import json
import socket
import re 
import uuid
import platform
#pip install psutil
#import psutil



#Variables
spec = str
#Classes
class blc():
    def __init__(self):
        self.blocks = [] 
        self.chain = []
        self.newblock(previushash = 1, proof = 100, data = 0)
        self.runningnode = self.getNodeInfo()
        self.lastblock = self.chain[len(self.chain)-1]
    
    def getNodeInfo(self):
        global spec
        info={}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['hostname']=socket.gethostname()
        info['ip-address']=socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()
        #info['memory'] = str(psutil.virtual_memory().total / (1024 **3))+ "GB"
        spec = info
        json_obj = json.dumps(info,indent=7)
        with open("node.json","w+") as f:
            f.write(json_obj)
        return info

    def newblock(self, previushash, proof, data):
        block = {

            'index' : len(self.chain)+1,
            'identifier' : self.prefix(len(self.chain)),
            'timestamp' : time(), #time() restituisce i secondi passati dal 1 Gennaio 1970 (epoca sitemi unix-like)
            'proof':proof,
            'previushash': previushash or self.hash(self.chain[-1]),
            'data': data,
            'datahash': self.datahash(data),
            'genblock' : self.genblock(previushash)
        }
        self.chain.append(block)
        self.blocks.append(block['identifier'])
        return block

    def datahash(self, dati):
        _dati = str(dati)
        hashlib.sha512(_dati.encode("utf-8"))

    @staticmethod
    def genblock(pv):
        if pv == 1:
            return True
        else:
            return False

    def prefix(self, _num):
        num_conv = str(_num)
        if len(num_conv) == 1:
            num_conv = "000" + num_conv
        if len(num_conv) == 2:
            num_conv = "00" + num_conv
        if len(num_conv) == 3:
            num_conv = "0" + num_conv
        prefix = num_conv[:-3] + "x" + num_conv[-3:]
        return prefix
        
    @staticmethod
    def hash(block):

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha512(block_string).hexdigest()

    def proof_of_work(self, last_block):

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            print(proof)
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"



blockchain = blc()


def mine():
    last_block = blockchain.lastblock
    proof = blockchain.proof_of_work(last_block)


    previous_hash = blockchain.hash(last_block)
    block = blockchain.newblock(proof, previous_hash, string)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['data'],
        'proof': block['proof'],
        'previou_shash': block['previushash'],
    }
    
    print(response)
#Video


print('''

Blockchain - Edoardo Santi

Command table type 'cmd'

''')
while True:
    init = input("Command >")

    if init == 'cmd':
        print('''
        Add block > addBlock
        To see all blocks > allBlocks
        To see all blocks identifiers > blocksIdentifiers
        To see the last block > lastBlock
        To see the running node > nodeInfo
        To quit > q or exit

        ''')
    elif init == 'addBlock':
        print("Insert the string that will be added in the block")
        print("When you press enter the block will be calculated, it can take a while, don't worry")
        string = input()
        blockchain.newblock(blockchain.hash(blockchain.chain[-1]), 100, string)
        mine()
    elif init == 'allBlocks':
        print("All blocks are")
        print(str(blockchain.chain))
    elif init == 'blocksIdentifiers':
        print("Blocks with identifiers")
        print(str(blockchain.blocks))
    elif init == 'lastBlock':
        print("Last block")
        print(str(blockchain.lastblock))
    elif init == 'nodeInfo':
        print("Node info")
        print(str(blockchain.runningnode))
    elif init == 'q' or init == 'exit':
        print("Saving files")
        json_obj = json.dumps(blockchain.blocks, indent=len(blockchain.blocks))
        with open("blocs.json",'w+') as b:
            b.write(json_obj)
        json_obj2 = json.dumps(blockchain.chain, indent=len(blockchain.chain))
        with open("chain.json",'w+') as b:
            b.write(json_obj2)
        json_obj3 = json.dumps(blockchain.lastblock, indent=len(blockchain.lastblock))
        with open("blocs.json",'w+') as b:
            b.write(json_obj3)
        exit()
