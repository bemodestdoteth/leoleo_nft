pragma solidity ^0.5.6;

import "./utils/Strings.sol";
import "./klaytn-contracts/ownership/Ownable.sol";
import "./klaytn-contracts/token/KIP17/KIP17Full.sol";
import "./klaytn-contracts/token/KIP17/KIP17Mintable.sol";

// 온체인 트리거 기반 가변 URI를 가진 NFT의 샘플 구현
contract LeoLeo_mint is KIP17Full("leoleo", "LeoLeo"), KIP17Mintable, Ownable {

    string private baseURI;
    string private notRevealedURI;
    string private URIExtension = ".json";

    bool public revealed = false;
    bool public paused = false;

    //발행 한도
    uint256 public mintLimit = 123;
    uint256 public batchMintLimit = 2;
    uint256 public mintcost = 1 ether;

    constructor(string memory _baseURI, string memory _initNotRevealedURI) public 
    {
        baseURI = _baseURI;
        setNotRevealedURI(_initNotRevealedURI);
    }

    //특정 토큰의 Uri index를 기반으로 적절한 URI를 리턴
    //Reveal되지 않았을 때는 reveal되지 않은 URI를 리턴
    function tokenURI(uint256 tokenId) public view returns (string memory)
    {
        require(_exists(tokenId), "KIP17Metadata: URI query for nonexistent token");
        if (!revealed)
        {
            return string(abi.encodePacked(notRevealedURI, Strings.fromUint256(tokenId), URIExtension));
        }
        return string(abi.encodePacked(baseURI, Strings.fromUint256(tokenId), URIExtension));
    }

    function setBaseURI(string memory _uri) public onlyOwner
    {
        baseURI = _uri;
    }

    //Reveal되지 않았을 때 참조할 URI 저장
    function setNotRevealedURI(string memory _uri) public onlyOwner
    {
        notRevealedURI = _uri;
    }

    function mint(address _to, uint256 _tokenId) public onlyMinter payable returns (bool)
    {
        require(!paused, "Minting has paused.");
        require(totalSupply() < mintLimit, "Mint limit exceeded");
        require(getBalance() >= mintcost, "Mint failed, not enough balance");
        
        bool result = super.mint(_to, _tokenId);
        require(result, "Minting failed.");
    }

    function batchMint(address to, uint256[] calldata tokenId) external onlyMinter payable
    {
        require(!paused, "Minting has paused.");
        require(tokenId.length <= batchMintLimit, "Mint limit per tx exceeded");
        require(getBalance() >= mintcost * tokenId.length, "Mint failed, not enough balance");
        for (uint256 i = 0; i < tokenId.length; i++)
        {
            mint(to, tokenId[i]);
        }
    }

    function batchTransfer(address to, uint256[] calldata tokenId) external
    {
        for (uint256 i = 0; i < tokenId.length; i ++)
        {
            transferFrom(msg.sender, to, tokenId[i]);
        }
    }

    function exists(uint256 tokenId) public view returns (bool)
    {
        return _exists(tokenId);
    }

    function tokensOfOwner(address owner) public view returns (uint256[] memory)
    {
        return _tokensOfOwner(owner);
    }

    function getBalance() public view returns (uint){ 
        return msg.sender.balance; 
    }

    function reveal() public onlyOwner
    {
        revealed = true;
    }

    function pause(bool _state) public onlyOwner
    {
        paused = _state;
    }

    function withdraw(uint256 amount) public payable onlyOwner
    {
        // Test code
        amount = msg.value;
        msg.sender.transfer(msg.value);
        //(bool os, ) = payable(owner()).call{value: address(this).balance}("");
        //require(os);
    }
}