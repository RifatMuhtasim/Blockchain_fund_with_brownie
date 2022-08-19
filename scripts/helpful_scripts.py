from re import L
from brownie import network, accounts, MockV3Aggregator
import os 
from web3 import Web3

Forked_blockchain = ["mainnet-fork", "mainnet-fork-dev"]
Local_blockchain = ["development", "ganache-local"]

def get_account():
     if(network.show_active() in Local_blockchain or network.show_active() in Forked_blockchain ):
          return accounts[0]
     else:
          return accounts.add(os.getenv("PRIVATE_KEY"))


def deploy_mock_aggregator():
     print(f"The Network is {network.show_active()}")
     if len(MockV3Aggregator) <= 0:
          print("Mock Deploying . . .")
          MockV3Aggregator.deploy(8, 200000000000, {"from": get_account()})