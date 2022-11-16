from web3 import Web3
import json
import time
import random
import matplotlib.pyplot as plt

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545", request_kwargs={"timeout": 1800}))

print(w3.isConnected())
# print(w3.eth.get_block('latest'))
# makeVouch(accounts[2], private_keys[2], accounts[3])


def makeVouch(contract, from_acc, to_acc):
    start = time.time()

    nonce = w3.eth.getTransactionCount(from_acc)
    tx = {
        "nonce": nonce,
        "from": from_acc,
        # "to": to_acc,
        "value": w3.toWei(1, "ether"),
        # "gas": 2000000,
        # "gasPrice": w3.toWei(50, "gwei"),
    }

    txn_hash = contract.functions.purchase_vouchToken().transact(tx)
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash.hex(), timeout=5400)

    nonce = w3.eth.getTransactionCount(from_acc)
    tx = {
        # "nonce": nonce,
        "from": from_acc,
        # "to": to_acc,
        "value": w3.toWei(0, "wei"),
        # "gas": 2000000,
        # "gasPrice": w3.toWei(50, "gwei"),
    }

    txn_hash = contract.functions.makeVouch(to_acc).transact(tx)
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash.hex(), timeout=5400)
    print(txn_receipt)

    end = time.time()

    return end - start


# Opening JSON file
f = open("/Users/teera/Desktop/Dissertation/evaluation/abi.json")
abi = json.load(f)
f2 = open("/Users/teera/Desktop/Dissertation/evaluation/bytecode.json")
# bytecode = "json.load(f2)"
contractAddress = "0xF3e71fFBd27D0e4bEEedc2CA290A63A03671CD7C"
contract = w3.eth.contract(address=contractAddress, abi=abi)

# respond_time = []
# num_nodes = []

# for i in range(0, 10):
#     for j in range(0, 10):
#         if i != j:
#             respond_time.append(
#                 makeVouch(contract, w3.eth.accounts[i], w3.eth.accounts[j])
#             )
#             num_nodes.append(contract.functions.getNodesCount().call())

# print(respond_time)
# print()
# print(num_nodes)

# plt.plot(respond_time, num_nodes)
# plt.show()

# 50 / 100 Node set
# for k in range(0,40):
#     w3.eth.account.create()

respond_time2 = []
num_nodes2 = []
print(respond_time2)
print(num_nodes2)
import random
voucher_list = random.sample(range(0,99),40)
for i in voucher_list:
    import random
    random_vouch = random.sample(range(0,99),random.randint(1,2))
    for j in random_vouch:
        if i != j:
            respond_time2.append(
                makeVouch(contract, w3.eth.accounts[i], w3.eth.accounts[j])
            )
    if len(respond_time2) == 75:
        break

            #num_nodes2.append(contract.functions.getNodesCount().call())

print(respond_time2)
# print()
#print(num_nodes2)

# plt.plot(respond_time2, num_nodes2)
# plt.show()
