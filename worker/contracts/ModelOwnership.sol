// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract AIModelOwnership is ERC721 {
    
    using Counters for Counters.Counter;
    Counters.Counter private _modelIds;

    // Mapping from model ID to IPFS CID
    mapping(uint256 => string) private _modelURIs;

    // Mapping from model ID to category
    mapping(uint256 => string) private _modelCategories;

    // Array to store all the model IDs.
    uint256[] private _allModelIds;

    constructor() ERC721("AIModelOwnership", "AIMO") {}

    function mintModel(address recipient, string memory modelURI, string memory category)
        public
        returns (uint256)
    {
        _modelIds.increment();

        uint256 newModelId = _modelIds.current();
        _mint(recipient, newModelId);
        _setModelURI(newModelId, modelURI);
        _setModelCategory(newModelId, category);
        
        // Add the model ID to the _allModelIds array.
        _allModelIds.push(newModelId);

        return newModelId;
    }

    function _setModelURI(uint256 modelId, string memory _modelURI) internal virtual {
        require(_exists(modelId), "ERC721URIStorage: URI set of nonexistent model");
        _modelURIs[modelId] = _modelURI;
    }

    function _setModelCategory(uint256 modelId, string memory _category) internal virtual {
        require(_exists(modelId), "ERC721Metadata: Category set of nonexistent model");
        _modelCategories[modelId] = _category;
    }

    function getModelURI(uint256 modelId) public view virtual returns (string memory) {
        require(_exists(modelId), "ERC721URIStorage: URI query for nonexistent model");

        string memory _modelURI = _modelURIs[modelId];
        return _modelURI;
    }

    function modelCategory(uint256 modelId) public view virtual returns (string memory) {
        require(_exists(modelId), "ERC721Metadata: Category query for nonexistent model");

        string memory _modelCategory = _modelCategories[modelId];
        return _modelCategory;
    }

    // Returns the total amount of models registered by the contract
    function totalSupply() public view returns (uint256) {
        return _allModelIds.length;
    }

    // Returns a model ID at a given index of all the models in this contract
    // Reverts if index is greater or equal to the total number of models
    function modelByIndex(uint256 index) public view returns (uint256) {
        require(index < totalSupply(), "ERC721Enumerable: global index out of bounds");
        return _allModelIds[index];
    }
}
