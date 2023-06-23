// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.15;

contract BookKeeping {
    address public owner;
    uint256 private _stakeValue;

    // event for EVM logging
    event CustomerPaid(address indexed cutomerAddress, uint256 value);

    mapping(address => uint256) public balances;

    // modifier to check if caller is owner
    modifier isOwner() {
        // If the first argument of 'require' evaluates to 'false', execution terminates and all
        // changes to the state and to Ether balances are reverted.
        // This used to consume all gas in old EVM versions, but not anymore.
        // It is often a good idea to use 'require' to check if functions are called correctly.
        // As a second argument, you can also provide an explanation about what went wrong.
        require(msg.sender == owner, "Caller is not owner");
        _;
    }

    constructor() {
        owner = msg.sender;
        _stakeValue = 1e17;
    }

    function balanceOf(
        address _address
    ) public view returns (uint256 _balance) {
        _balance = balances[_address];
    }

    // staking function, can be called by anyone
    function stake() external payable {
        require(msg.value >= _stakeValue, "not enough eth to be staked");
        balances[msg.sender] += msg.value;
    }

    // this is the function that should be called by consumer for paying the computation cost
    function consumerPay() external payable {
        // undistributed eth are temporarily stored in owner's account
        balances[owner] += msg.value;
        emit CustomerPaid(msg.sender, msg.value);
    }

    // distribute reward to node address, can only be called by owner
    function distributeReward(address _address, uint256 _value) public isOwner {
        require(balances[owner] >= _value);
        balances[owner] -= _value;
        balances[_address] += _value;
    }

    // default receive func, money goes to owner account
    receive() external payable {
        balances[owner] += msg.value;
    }

    // owner can take away the stakedValue of a node for bad behaviour, remaining balance returned.
    function slash(address payable _address) public isOwner {
        require(balances[_address] >= _stakeValue);
        uint remainingBalance = balances[_address] - _stakeValue;
        balances[owner] += _stakeValue;
        balances[_address] = 0;
        _address.transfer(remainingBalance);
    }

    // withdraw function to be called by node for unstaking, or by owner to take profit.
    function withdraw() public {
        require(
            balances[msg.sender] > 0,
            "no eth in the sending account to be withrawed"
        );
        payable(msg.sender).transfer(balances[msg.sender]);
        balances[msg.sender] = 0;
    }

    function claim() public {
        require(
            balances[msg.sender] > _stakeValue,
            "not enough eth to be claimed"
        );
        payable(msg.sender).transfer(balances[msg.sender] - _stakeValue);
        balances[msg.sender] = balances[msg.sender] - _stakeValue;
    }
}
