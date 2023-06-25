# Artifex

This project is developed with hardhat and we used React for the frontend. In the backend we used stable-diffusion-web-ui to perform inference and use web3.py to listen to smart contract event and call smart contract functions. The result returned by backend is permanently stored to IPFS and the cid to the object is broadcasted as an event, which will be picked by frontend so that result can be rendered to end users.
You should be able to follow it by yourself by reading the README and exploring its
`contracts`, `tests`, `scripts` and `frontend` directories.

## Quick start

The first things you need to do are cloning this repository and installing its
dependencies:

```sh
cd artifex
npm install
```

Once installed, let's run Hardhat's testing network:

```sh
npx hardhat node
```

Then, on a new terminal, go to the repository's root folder and run this to
deploy your contract:

```sh
npx hardhat run scripts/deploy.js --network localhost
```

Finally, we can run the frontend with:

```sh
cd frontend
npm install
npm start
```

Open [http://localhost:3000/](http://localhost:3000/) to see your Dapp. You will
need to have [Coinbase Wallet](https://www.coinbase.com/wallet) or [Metamask](https://metamask.io) installed and listening to
`localhost 8545`, i.e. you need to manually add the hardhat test network into your wallet. It is likely that your default do not have any
balance on the hardhat test network, you can run:

```sh 
npx hardhat --network localhost faucet 0x6fcaa0b1c75fd19ae367e4eebf2e031be7a2accf
```

to add eth balance on the hardhat test network


### Running with local worker
Start the SD webui docker following this [guide](https://github.com/AbdBarho/stable-diffusion-webui-docker/wiki/Usage). 
Create ```credentials.json``` and  save your credentials.
Then go to /hardhat-boilerplate/scripts/ and run
```
python worker_node.py
```
to start the python worker node program.
