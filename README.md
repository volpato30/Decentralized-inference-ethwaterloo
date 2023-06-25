# Hardhat Boilerplate

This repository contains a sample project that you can use as the starting point
for your Ethereum project. It's also a great fit for learning the basics of
smart contract development.

This project is intended to be used with the
[Hardhat Beginners Tutorial](https://hardhat.org/tutorial), but you should be
able to follow it by yourself by reading the README and exploring its
`contracts`, `tests`, `scripts` and `frontend` directories.

## Quick start

The first things you need to do are cloning this repository and installing its
dependencies:

```sh
cd hardhat-boilerplate
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
Start the SD webui docker following this [guide](https://github.com/AbdBarho/stable-diffusion-webui-docker/wiki/Usage). Then go to /hardhat-boilerplate/scripts/ and run
```
python event_listening.py
```
to start the python backend program.