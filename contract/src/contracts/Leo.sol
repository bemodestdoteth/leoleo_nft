pragma solidity ^0.8.0;

import "./ERC721.sol";
contract Leo is ERC721
{
    constructor () ERC721("Leo", "LEO") public {}

    // _color: to tell solidity that it's a local variable.
    function mintLeo(string memory _color) public
    {

    }
}