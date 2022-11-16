
# Blockchain-based reputation system with Pagerank algorithm

This is the dissertation project in partial fulfilment of degree of MSc. Data science, University of Southampton.


## Authors

- [@Teeraphon_Issaranuluk](https://github.com/teeraphon)


## About project

This master’s thesis examines the proof-of-concept prototype
of a blockchain-based reputation system using the Pagerank algorithm to compute
the reputation score. It presents a system of smart contracts that establish interaction
logic and model trust among the system’s pseudo-anonymous identities. The contract
is installed on a blockchain network that computes, stores, and updates the reputation
score of entities. The suggested technique and trust metrics are tested by replicating an
interaction network with a different degree of node number and transaction randomness.
The research findings demonstrate that the suggested strategy is to perform efficiently
in a small simulation network in performance and rank accuracy.
## Main features

- Vouch machanism
- Vouch detaching mechanism
- Node deletion mechanism
- Pagerank calculation mechanism
- Penalties mechanism


## Project dependencies
Ehtereum (Solidity), Ganache, Truffle, Web3



## Installation

Install Ganache as Ehtereum development environment

```bash
  npm install -g ganache
```

```bash
  ganache -p 9000
```

Install Truffle as testing framework

```bash
  npm install -g truffle
```

```bash
  truffle v
```

Install Web3 as experiment framework

```bash
  npm install web3
```
    
