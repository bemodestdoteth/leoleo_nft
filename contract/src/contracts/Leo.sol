pragma solidity ^0.8.0;

import "./ERC721.sol";

contract Leo is ERC721
{
    address owner;

    constructor () ERC721("Leo", "LEO") public
    {
        owner = msg.sender;
    }

    modifier onlyOwner()
    {
        require(owner == msg.sender, "Ownable: caller is not the owner."); _;
    }

    // _color: to tell solidity that it's a local variable.
    function mintLeo(string memory _tokenURI, address _recipient) public onlyOwner returns(uint256)
    {
        uint256 _newItemId = 1;
        _mint(_recipient, _newItemId);
        _setTokenURI(_newItemId, _tokenURI);

        return _newItemId;
    }
}