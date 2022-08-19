from brownie import Fund_me
from scripts.helpful_scripts import get_account


def Fund():
     fund_me = Fund_me[-1]
     account = get_account()
     print('Funding ...', fund_me)
     get_entrance_fee = fund_me.get_entrance_fee()
     fund_me.fund({"from": account, "value": get_entrance_fee})


def Withdraw():
     fund_me = Fund_me[-1]
     account = get_account()
     print("Withdraw ...")
     fund_me.withdraw({"from": account})


def main():
     Fund()
     Withdraw()