pragma solidity ^0.7.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract Leo is ERC721
{
    address owner;
    string public baseURI = "https://leometadata.s3.ap-northeast-2.amazonaws.com/images/metadata/";
    string public baseExtension = ".json";
    string public notRevealedUri = "not revealed amazon s3 uri";
    string public _name = name();
    string public _symbol = symbol();
    uint256 public cost = 0.05 ether;
    uint256 public maxSupply = 123;
    uint256 public maxMintAmount = 2;
    bool public paused = false;
    bool public revealed = false;
    mapping(address => bool) public whitelisted;

    constructor () ERC721("Leo", "LEO") public
    {
        owner = msg.sender;
        mint(msg.sender, 5); // For test purpose
    }

    modifier onlyOwner()
    {
        require(owner == msg.sender, "Ownable: caller is not the owner."); _;
    }

    // internal
    function _baseURI() internal view virtual override returns (string memory)
    {
        return baseURI;
    }

    function tokenURI(uint256 tokenId) public view returns (string memory) {
        require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");

        if (!revealed)
        {
            return notRevealedUri;
        }

        return bytes(_baseURI()).length > 0 ? string(abi.encodePacked(_baseURI(), tokenId.toString())) : "";
    }
    
    // enumerate all of ``owner``'s tokens.
    function tokensfromWallet(address _owner) public view returns (uint256[] memory)
    {
        uint256 ownerTokenCount = balanceOf(_owner);
        uint256[] memory tokenIds = new uint256[](ownerTokenCount);
        for (uint256 i; i < ownerTokenCount; i++) {
        tokenIds[i] = tokenOfOwnerByIndex(_owner, i);
        }
        return tokenIds;
    }    

    function mint(address _recipient, uint256 _mintAmount) public payable
    {
        uint256 supply = totalSupply();
        require(!paused);
        require(_mintAmount > 0);
        require(_mintAmount <= maxMintAmount);
        require(supply + _mintAmount <= maxSupply);

        if (msg.sender != owner) {
            if(whitelisted[msg.sender] != true) {
            require(msg.value >= cost * _mintAmount);
            }
        }

        for (uint256 i = 1; i <= _mintAmount; i++) {
        _safeMint(_recipient, supply + i);
        }
    }

    // onlyOwner
    function reveal() public onlyOwner {
        revealed = true;
    }

    function setCost(uint256 _newCost) public onlyOwner {
        cost = _newCost;
    }

    function pause(bool _state) public onlyOwner {
        paused = _state;
    }

    function setmaxMintAmount(uint256 _newmaxMintAmount) public onlyOwner {
        maxMintAmount = _newmaxMintAmount;
    }

    function setBaseExtension(string memory _newBaseExtension) public onlyOwner {
        baseExtension = _newBaseExtension;
    }
    
    function whitelistUser(address _user) public onlyOwner {
        whitelisted[_user] = true;
    }
 
    function removeWhitelistUser(address _user) public onlyOwner {
        whitelisted[_user] = false;
    }

    function withdraw() public payable onlyOwner
    {
        (bool os, ) = payable(owner).call{value: address(this).balance}("");
        require(os);
  }
}