from brownie import Fund_me, network, accounts, exceptions
from scripts.helpful_scripts import get_account, Local_blockchain
from scripts.deploy import DeployFundMe
import pytest


def test_can_fund_and_withdraw():
     account = get_account()
     fund_me = DeployFundMe()
     entrance_fee = fund_me.get_entrance_fee()
     tx = fund_me.fund({ "from": account, "value": entrance_fee})
     tx.wait(1)
     assert fund_me.address_to_amount_funded(account.address) == entrance_fee

     tx2= fund_me.withdraw({"from": account})
     tx2.wait(2)
     assert fund_me.address_to_amount_funded(account.address) == 0


def test_only_owner_can_withdraw():
     if network.show_active() not in Local_blockchain:
          pytest.skip("Only for local testing")

     fund_me = DeployFundMe()
     bad_actor = accounts.add()
     with pytest.raises(exceptions.VirtualMachineError):
          fund_me.withdraw({"from": bad_actor})