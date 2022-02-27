pragma solidity ^0.5.6;

import "./utils/Strings.sol";
import "./klaytn-contracts/ownership/Ownable.sol";
import "./klaytn-contracts/token/KIP17/KIP17Full.sol";
import "./klaytn-contracts/token/KIP17/KIP17Mintable.sol";

contract LeoLeo_mint is KIP17Full("leoleo-nft", "LeoLeo"), KIP17Mintable, Ownable {

    event Minted(address _to, uint256 _tokenId);

    string private baseURI;
    string private URIExtension = ".json";
    bool public paused = false;
    uint256 public mintLimit = 5; // 123
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

    function batchMint(address _to, uint256 _mintAmount) external onlyMinter
    {
        uint256 _tokenId = totalSupply() + 1;

        require(!paused, "PausedbyOwner: Minting has been paused by owner.");
        require(_mintAmount <= batchMintLimit, "LimitExceeded: Minting limit per transaction exceeded");
        for (uint256 i = 0; i < _mintAmount; i++)
        {
            require(!exists(_tokenId), "IdAlreadyExists: Token ID already exists in blockchain.");
            require(_tokenId <= mintLimit, "LimitExceeded: All tokens have been sold out.");
            mint(_to, _tokenId);
            emit Minted(_to, _tokenId);
            _tokenId++;
        }
    }

    function setBaseURI(string memory _uri) private onlyOwner
    {
        baseURI = _uri;
    }

    function burn(uint256 tokenId) public
    {
        _burn(tokenId);
    }

    function exists(uint256 tokenId) public view returns (bool)
    {
        return _exists(tokenId);
    }

    function tokensOfOwner(address owner) public view returns (uint256[] memory)
    {
        return _tokensOfOwner(owner);
    }

    function pause(bool _state) public onlyOwner
    {
        paused = _state;
    }
}