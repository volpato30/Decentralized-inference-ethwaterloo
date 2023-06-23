// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;

import "@openzeppelin/contracts/utils/structs/EnumerableMap.sol";

contract JobManager {
    using EnumerableSet for EnumerableSet.AddressSet;

    EnumerableSet.AddressSet private workers;

    event WorkerStaked(address indexed worker);
    event WorkerUnstaked(address indexed worker);
    event NewJobCreated(bytes indexed jobId, string prompt);
    event JobSubmitted(bytes32 indexed jobId, string[] nodes);

    mapping(string => string) public results;

    constructor() {
        // Initialize the results mapping
        results["address1"] = "QmS2zfKecFvgTSBBKKy9udkdY2yhjW7eTkc5rv5FL7hHL8";
        results["address2"] = "QmS2zfKecFvgTSBBKKy9udkdY2yhjW7eTkc5rv5FL7hHL8";
        results["address3"] = "QmS2zfKecFvgTSBBKKy9udkdY2yhjW7eTkc5rv5FL7hHL8";
    }

    function stake() public {
        workers.add(msg.sender);
        emit WorkerStaked(msg.sender);
    }

    function unstake() public {
        workers.remove(msg.sender);
        emit WorkerUnstaked(msg.sender);
    }

    function createJob(string memory _prompt) public {
        bytes memory jobId = abi.encodePacked(keccak256(abi.encodePacked(msg.sender, _prompt)));
        emit NewJobCreated(jobId, _prompt);
    }

    function submit(bytes32 _jobId, string[] memory _nodes) public {
        emit JobSubmitted(_jobId, _nodes);
    }

    function getWorkers() public view returns (address[] memory) {
        address[] memory workerList = new address[](workers.length());
        for (uint i = 0; i < workers.length(); i++) {
            workerList[i] = workers.at(i);
        }
        return workerList;
    }

}
