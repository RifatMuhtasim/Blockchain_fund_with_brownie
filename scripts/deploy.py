from unittest import mock
from brownie import Fund_me, network, config, MockV3Aggregator
from scripts.helpful_scripts import get_account, deploy_mock_aggregator, Local_blockchain


def DeployFundMe():
     account = get_account()

     if network.show_active() not in Local_blockchain :
          price_feed_address = config['networks'][network.show_active()]['eth_usd_price_feed']
     else:
          deploy_mock_aggregator()
          price_feed_address = MockV3Aggregator[-1].address

     fund_me = Fund_me.deploy(price_feed_address, {"from": account}, publish_source= config['networks'][network.show_active()].get('verify'))
     print(f"Brownie FundMe Deployed on {fund_me.address} ")
     return fund_me


def main():
     DeployFundMe()