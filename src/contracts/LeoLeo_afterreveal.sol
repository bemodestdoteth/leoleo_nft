pragma solidity ^0.5.6;

import "./utils/Strings.sol";
import "./klaytn-contracts/ownership/Ownable.sol";
import "./klaytn-contracts/token/KIP17/KIP17Full.sol";
import "./klaytn-contracts/token/KIP17/KIP17Mintable.sol";

contract LeoLeo_mint is KIP17Full("leoleo", "LeoLeo"), KIP17Mintable, Ownable {

    event Migrated(address _holder, uint256 _tokenId);

    address private unrevealedContract;
    string private baseURI;
    string private URIExtension = ".json";
    bool public paused = false;
    uint256 private deployedBlockNo;
    uint256 public mintLimit = 123;
    uint256 public batchMintLimit = 2;

    constructor(string memory _baseURI, address _unrevealedContract) public 
    {
        setBaseURI(_baseURI);
        setUnrevealedContract(_unrevealedContract);
        deployedBlockNo = block.number;
    }

    function tokenURI(uint256 tokenId) public view returns (string memory)
    {
        require(_exists(tokenId), "KIP17Metadata: URI query for nonexistent token");
        return string(abi.encodePacked(baseURI, Strings.fromUint256(tokenId), URIExtension));
    }

    function exists(uint256 tokenId) public view returns (bool)
    {
        return _exists(tokenId);
    }

    function tokensOfOwner(address owner) public view returns (uint256[] memory)
    {
        return _tokensOfOwner(owner);
    }

    function setBaseURI(string memory _uri) private onlyOwner
    {
        baseURI = _uri;
    }

    function setUnrevealedContract(address _unrevealedContract) private onlyOwner
    {
        unrevealedContract = _unrevealedContract;
    }

    function pause(bool _state) public onlyOwner
    {
        paused = _state;
    }

    function triggerMigration() public onlyOwner
    {
        require (block.number >= deployedBlockNo + 100);
        for (uint256 i = 1; i <= 5 /*mintLimit*/; i++)
        {
            migrate(i);
        }
    }

    function migrate(uint _tokenId) private onlyOwner
    {
        bool done = true;
        bytes memory data = "";

        (done, data) = unrevealedContract.call(abi.encodeWithSignature("ownerOf(uint256)", _tokenId));
        address holder = abi.decode(data, (address));

        // Mint and burn
        done = mint(holder, _tokenId);
        (done, data) = unrevealedContract.call(abi.encodeWithSignature("burn(uint256)", _tokenId));

        emit Migrated(holder, _tokenId);
    }
}