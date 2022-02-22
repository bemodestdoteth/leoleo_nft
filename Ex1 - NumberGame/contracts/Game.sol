pragma solidity >=0.4.24 <=0.5.6;

contract Ownable {
  address owner;
  constructor() public {
    owner = msg.sender;
  }

  modifier Owned {
    require(msg.sender == owner);
    _;
  }
}

contract Mortal is Ownable {
  function kill() public Owned { 
    selfdestruct(msg.sender);
  }
}


contract Game is Mortal {
  uint minBet; // 최소 베팅액  

  event Won(bool _result, uint _amount);

  constructor(uint _minBet) payable public {
    require(_minBet > 0);    
    minBet = _minBet;    
  }

  function() external { 
    revert();
  }

  function play(uint _num) payable public {
    require(_num > 0 && _num <= 5);
    require(msg.value >= minBet);

    uint winNum = random();
    if (_num == winNum) {
      uint amtWon = msg.value * 2;
      if(!msg.sender.send(amtWon)) revert();
      emit Won(true, amtWon);
    } else {
      emit Won(false, 0);
    }
  }

  function getBalance() Owned public view returns(uint) {
    return address(this).balance;
  }

  function random() public view returns (uint) {
    return uint(keccak256(abi.encodePacked(now, msg.sender))) % 5 + 1;
  }
}