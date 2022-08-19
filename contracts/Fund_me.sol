// SPDX-License-Identifier: MIT 
pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";


contract Fund_me{
     using SafeMathChainlink for uint256;

     mapping (address => uint256) public address_to_amount_funded;
     address[] public funders;
     address public owner;
     AggregatorV3Interface public price_feed;

     constructor( address _price_feed) public {
          owner = msg.sender;
          price_feed = AggregatorV3Interface(_price_feed);
     }

     function fund() public payable {
          uint256 minimum_usd = 10 * 10 * 18;
          require(get_conversion_rate(msg.value) >= minimum_usd, "You need to spend more ETH!");
          address_to_amount_funded[msg.sender] += msg.value;
          funders.push(msg.sender);
     }

     function get_entrance_fee() public view returns(uint256){
          // minimum USD
          uint256 minimum_usd = 50 * 10 ** 18;
          uint256 price= get_price();
          uint256 precision = 1 * 10 ** 18;
          return (minimum_usd * precision)/price;
     }

     function get_version() public view returns (uint256){
          return price_feed.version();          
     }

     function get_price() public view returns(uint256){ 
          (, int256 answer,,,) = price_feed.latestRoundData();
          return uint256(answer * 10000000000);
     }

     function get_conversion_rate(uint256 eth_amount) public view returns(uint256){
          uint256 eth_price = get_price();
          uint256 eth_amount_in_usd = (eth_price * eth_amount) / 1000000000000000000;
          return eth_amount_in_usd;
     }
     
     modifier only_owner {
          require(msg.sender == owner);
          _;
     }

     function withdraw() payable only_owner public{
          msg.sender.transfer(address(this).balance);
          for(uint256 funder_index=0; funder_index < funders.length; funder_index++){
               address funder = funders[funder_index];
               address_to_amount_funded[funder] =0;
          }
          funders = new address[](0);
     }

}