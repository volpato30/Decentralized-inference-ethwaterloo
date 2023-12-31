// This is a script for deploying your contracts. You can adapt it to deploy
// yours, or create new ones.

const path = require("path");

async function main() {
  // This is just a convenience check
  if (network.name === "hardhat") {
    console.warn(
      "You are trying to deploy a contract to the Hardhat Network, which" +
        "gets automatically created and destroyed every time. Use the Hardhat" +
        " option '--network localhost'"
    );
  }

  // ethers is available in the global scope
  const [deployer] = await ethers.getSigners();
  console.log(
    "Deploying the contracts with the account:",
    await deployer.getAddress()
  );

  console.log("Account balance:", (await deployer.getBalance()).toString());

  const ModelOwnership = await ethers.getContractFactory("AIModelOwnership");
  const modelOwnership = await ModelOwnership.deploy();
  await modelOwnership.deployed();

  const JobManager = await ethers.getContractFactory("JobManager");
  const jobManager = await JobManager.deploy(modelOwnership.address);
  await jobManager.deployed();

  console.log("model ownership contract address:", modelOwnership.address);
  console.log("jobManager contract address:", jobManager.address);

  // We also save the contract's artifacts and address in the frontend directory
  saveFrontendFiles(modelOwnership, jobManager);
}

function saveFrontendFiles(modelOwnership, jobManager) {
  const fs = require("fs");
  const contractsDir = path.join(__dirname, "..", "frontend", "src", "contracts");

  if (!fs.existsSync(contractsDir)) {
    fs.mkdirSync(contractsDir);
  }

  fs.writeFileSync(
    path.join(contractsDir, "contract-address.json"),
    JSON.stringify({ AIModelOwnership: modelOwnership.address, JobManager: jobManager.address}, undefined, 2)
  );

  const modelOwnershipArtifact = artifacts.readArtifactSync("AIModelOwnership");
  const jobManagerArtifact = artifacts.readArtifactSync("JobManager");

  fs.writeFileSync(
    path.join(contractsDir, "AIModelOwnership.json"),
    JSON.stringify(modelOwnershipArtifact, null, 2)
  );
  fs.writeFileSync(
    path.join(contractsDir, "JobManager.json"),
    JSON.stringify(jobManagerArtifact, null, 2)
  );
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
