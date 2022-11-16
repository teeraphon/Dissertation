from web3 import Web3
import json
import time
import matplotlib.pyplot as plt
import random

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545", request_kwargs={"timeout": 1800}))
import networkx as nx

# Connect to Ganache
print(w3.isConnected())


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
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash.hex(), timeout=1800)
    # print(from_acc)
    # print(to_acc)
    # print(txn_receipt)
    # print()

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
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash.hex(), timeout=1800)
    print(txn_receipt)

    end = time.time()

    return end - start


def genRandomEdges(num_edges, num_nodes):
    edges = []
    i = 0
    while i < num_edges:
        u = random.choice(range(num_nodes))
        v = random.choice(range(num_nodes))
        if u != v and (u, v) not in edges:
            edges.append((u, v))
            i += 1
    return edges


# Opening JSON file
f = open("/Users/teera/Desktop/Dissertation/project/evaluation/abi.json")
abi = json.load(f)
f2 = open("/Users/teera/Desktop/Dissertation/project/evaluation/bytecode.json")
# bytecode = "json.load(f2)"
# Set contract address
contractAddress = "0xEAcb0C3812DD6d6bbE0D8fAb7d089B6E10D2b158"
# Connect to smart contract
contract = w3.eth.contract(address=contractAddress, abi=abi)

edges = [
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (0, 5),
    (0, 6),
    (0, 7),
    (1, 8),
    (1, 9),
    (1, 3),
    (1, 5),
    (1, 6),
    # (2, 1),
    # (2, 4),
    # (2, 7),
    # (2, 8),
    # (2, 9),
    # (3, 2),
    # (3, 4),
    # (3, 8),
    # (3, 9),
    # (4, 5),
    # (4, 6),
    # (5, 1),
    # (5, 7),
    # (5, 8),
]

edges = genRandomEdges(10, 10)
#########################################################################
# Smart Contract
#########################################################################
# Make Vouch
for i, j in edges:
    makeVouch(contract, w3.eth.accounts[i], w3.eth.accounts[j])

# Get scores based on addresses
scores = {}
for i in range(10):
    score = contract.functions.get_scores(w3.eth.accounts[i]).call()
    scores[w3.eth.accounts[i]] = score
print("Smart Contract")
scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}
for k, v in scores.items():
    print(f"{k}: {v}")

#########################################################################
# Python Page Ranking
#########################################################################

G = nx.DiGraph()
nodes = []
for i, j in edges:
    if w3.eth.accounts[i] not in nodes:
        G.add_node(w3.eth.accounts[i])
        nodes.append(w3.eth.accounts[i])
    if w3.eth.accounts[j] not in nodes:
        G.add_node(w3.eth.accounts[j])
        nodes.append(w3.eth.accounts[j])
    G.add_edge(w3.eth.accounts[i], w3.eth.accounts[j])
pr = nx.pagerank(G)
print("Normal Page Ranking")
pr = {k: v for k, v in sorted(pr.items(), key=lambda item: item[1])}
for k, v in pr.items():
    print(f"{k}: {v}")

print(f"number_of_edges: {G.number_of_edges()}")

pos = nx.spiral_layout(G)
nx.draw(G, pos, with_labels=True, node_color="#f86e00")
x_values, y_values = zip(*pos.values())
x_max = max(x_values)
x_min = min(x_values)
x_margin = (x_max - x_min) * 1.5
plt.xlim(x_min - x_margin, x_max + x_margin)
plt.show()
