pragma solidity ^0.5.6;

import "./utils/Strings.sol";
import "./klaytn-contracts/ownership/Ownable.sol";
import "./klaytn-contracts/token/KIP17/KIP17Full.sol";
import "./klaytn-contracts/token/KIP17/KIP17Mintable.sol";

contract LeoLeo_mint is KIP17Full("leoleo", "LeoLeo"), KIP17Mintable, Ownable {

    event Minted(address _to, uint256 _tokenId);

    address private burnAddress = 0x000000000000000000000000000000000000dEaD;
    string private baseURI;
    string private URIExtension = ".json";
    bool public paused = false;
    uint256 public mintLimit = 123;
    uint256 public batchMintLimit = 2;

    constructor(string memory _baseURI) public 
    {
        setBaseURI(_baseURI);
    }

    function tokenURI(uint256 tokenId) public view returns (string memory)
    {
        require(_exists(tokenId), "KIP17Metadata: URI query for nonexistent token");
        return string(abi.encodePacked(baseURI, Strings.fromUint256(tokenId), URIExtension));
    }

    function mint(address _to, uint256 _tokenId) public onlyMinter returns (bool)
    {
        require(!paused, "Minting has paused.");
        require(totalSupply() < mintLimit, "Mint limit exceeded");
        
        super.mint(_to, _tokenId);
        emit Minted(_to, _tokenId);
    }

    function batchMint(address _to, uint256[] calldata _tokenId) external onlyMinter
    {
        require(!paused, "Minting has paused.");
        require(_tokenId.length <= batchMintLimit, "Mint limit per tx exceeded");
        for (uint256 i = totalSupply(); i < _tokenId.length; i++)
        {
            mint(_to, _tokenId[i]);
            emit Minted(_to, _tokenId[i]);
        }
    }

    function burn(address _from, uint256 tokenId) private onlyOwner
    {
        transferFrom(_from, burnAddress, tokenId);
    }

    function setBaseURI(string memory _uri) private onlyOwner
    {
        baseURI = _uri;
    }

    function exists(uint256 tokenId) public view returns (bool)
    {
        return _exists(tokenId);
    }

    function tokensOfOwner(address owner) public view returns (uint256[] memory)
    {
        return _tokensOfOwner(owner);
    }

    function pause(bool _state) private onlyOwner
    {
        paused = _state;
    }
}