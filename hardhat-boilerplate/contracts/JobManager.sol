// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;

import "@openzeppelin/contracts/utils/structs/EnumerableMap.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

interface IAIModelOwnership {
    function ownerOf(uint256 tokenId) external view returns (address owner);
}
contract JobManager {

    event NewJobCreated(address indexed workerAddress, uint256 jobId, uint256 modelId, string prompt);
    event JobSubmited(address indexed workerAddress,uint256 jobId, uint256 modelId, string prompt, string resultCid);

    enum Status {
        Waiting,
        Finished
    }

    struct Job {
        uint256 jobId;
        uint256 modelId;
        uint256 createTime;
        address owner;
        address worker;
        string prompt;
        string resultCid;
        Status status;
    }

    mapping(address => uint256) public balances;
    uint256 private _stakeValue = 0.1 ether;

    address public modelOwnershipContractAddress;
    IAIModelOwnership private _modelOwnership;

    using EnumerableSet for EnumerableSet.AddressSet;
    EnumerableSet.AddressSet private _workers;

    address public owner;

    Job[] public jobs;

    using Counters for Counters.Counter;
    Counters.Counter private _jobIds;

    mapping (uint => address) public jobToConsumer;
    mapping (address => uint) _ownerJobCount;

    uint _computationJobFee = 0.001 ether;

    constructor(address ownershipContractAddress) {
        modelOwnershipContractAddress = ownershipContractAddress;
        _modelOwnership = IAIModelOwnership(ownershipContractAddress);
        owner = msg.sender;
    }

    // modifier to check if caller is owner
    modifier isOwner() {
        require(msg.sender == owner, "Caller is not owner");
        _;
    }

    // This function creates a new Job and assign the job to a rondom works. 
    // Caller(consumer) should also pay for the computational cost.

    function createNewJob(uint256 modelId, string calldata prompt) external payable {
        require(msg.value >= _computationJobFee, "Not enough computation fee");
        // Check if the modelId exists in the AIModelOwnership contract
        require(_modelOwnership.ownerOf(modelId) != address(0), "Invalid modelId");
        balances[owner] += msg.value;

        address worker = _pickRandomWorker();

        _jobIds.increment();
        uint256 jobId= _jobIds.current();
        
        Job memory job = Job(jobId, modelId, uint256(block.timestamp), msg.sender, worker, prompt,'', Status.Waiting);
        jobs.push(job);
        _ownerJobCount[msg.sender]++;
        jobToConsumer[jobId] = msg.sender;
        emit NewJobCreated(worker,jobId,modelId,prompt);
    }


    // This function is used for workers to submit their Job computation result.
    function submitJob(string calldata cid, uint256 jobId) external {
        require(msg.sender == jobToConsumer[jobId], "only assigned worker can submit job result");
        Job storage job = jobs[jobId-1];
        job.resultCid = cid;
        job.status = Status.Finished;
        emit JobSubmited(msg.sender, job.jobId, job.modelId, job.prompt, cid);
    }

    function getJobsByOwner() external view returns(uint256[] memory) {
        uint256[] memory result = new uint256[](_ownerJobCount[msg.sender]);
        uint counter = 0;
        for (uint i = 0; i < jobs.length; i++) {
        if (jobToConsumer[i] == msg.sender) {
            result[counter] = i;
            counter++;
            }
        }
        return result;
  }

    function _pickRandomWorker() private view returns (address) {
        require(_workers.length() > 0, "No worker added yet");
        uint256 randomIndex = _random() % _workers.length();
        return _workers.at(randomIndex);
    }

    function _random() private view returns (uint256) {
        return uint256(keccak256(abi.encodePacked(block.timestamp)));
    }

    function _refundIfOver(uint256 total) private {
        require(msg.value >= total, "Invalid value.");
        if (msg.value > total) {
            payable(msg.sender).transfer(msg.value - total);
        }
    }

    // staking function, can be called by anyone
    function stake() external payable {
        require(msg.value >= _stakeValue, "not enough eth to be staked");
        balances[msg.sender] += msg.value;
        _workers.add(msg.sender);
    }

    function unstake() public {
        require(
            balances[msg.sender] > 0,
            "no eth in the sending account to be withrawed"
        );
        payable(msg.sender).transfer(balances[msg.sender]);
        balances[msg.sender] = 0;
        _workers.remove(msg.sender);
    }

    function balanceOf(
        address _address
    ) public view returns (uint256 _balance) {
        _balance = balances[_address];
    }

    // distribute reward to node address, can only be called by owner
    function distributeReward(address _address, uint256 _value) public isOwner {
        require(balances[owner] >= _value);
        balances[owner] -= _value;
        balances[_address] += _value;
    }
}