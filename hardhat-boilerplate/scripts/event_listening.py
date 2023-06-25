import json
from web3 import Web3
import requests
import asyncio
import logging
import boto3
from botocore.exceptions import ClientError
import base64
import os
import json
import copy
# add your blockchain connection information
hardhat_rpc = "http://127.0.0.1:8545/"
web3 = Web3(Web3.HTTPProvider(hardhat_rpc))

sd_url = "http://127.0.0.1:7860/sdapi/v1/txt2img/"

with open("credentials.json", "r") as f:
    u = json.load(f)
    caller = u["address"]
    private_key = u["privateKey"]

with open("txt2img_config.json", "r") as f:
    SEARCH_CONFIG = json.load(f)

with open("../frontend/contracts/contract-address.json", "r") as f:
    u = json.load(f)
    contract_address = u["JobManager"]
with open("../frontend/src/contracts/JobManager.json", "r") as f:
    contract_obj = json.load(f)
contract_abi = contract_obj["abi"]
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
# initialize the chain id, we need it to build the transaction for replay protection
Chain_id = web3.eth.chain_id

CHAIN_SAFE_KEY_ID = 'MHHARRNNQMSRDZECLSBN'
CHAIN_SAFE_API_KEY = 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODc1NzE2NjYsImNuZiI6eyJqa3UiOiIvY2VydHMiLCJraWQiOiI5aHE4bnlVUWdMb29ER2l6VnI5SEJtOFIxVEwxS0JKSFlNRUtTRXh4eGtLcCJ9LCJ0eXBlIjoiYXBpX3NlY3JldCIsImlkIjoxMjk0MCwidXVpZCI6ImI5NWE3ZGJkLTViOWEtNGYwYy1hZjA3LTU3YWFlNjE3YmQ2ZCIsInBlcm0iOnsiYmlsbGluZyI6IioiLCJzZWFyY2giOiIqIiwic3RvcmFnZSI6IioiLCJ1c2VyIjoiKiJ9LCJhcGlfa2V5IjoiTUhIQVJSTk5RTVNSRFpFQ0xTQk4iLCJzZXJ2aWNlIjoic3RvcmFnZSIsInByb3ZpZGVyIjoiIn0.Te0Qu_vx1RVBKFHOVeGsI62QwBGC7fYWvItPK-QvxQGBbRDMD-WXWSwgKj00YXi6o315FssiePXovPTzqzry1g'
CHAIN_SAFE_ENDPOINT = 'https://buckets.chainsafe.io'
CHAIN_SAFE_BUCKET_NAME = 'Artifex'

CHAIN_SAFE_S3_KEY = 'R2W8Tg8p0ZhYkDf4qrZed8jbA4T6obfeICQfQyfu'
CHAIN_SAFE_S3_ID = 'YJCJAJFUGJVKXTMHYDTF'

CHAIN_SAFE_API= 'https://api.chainsafe.io/api/v1/bucket/d65358b3-ea8d-4c77-b529-f9ba403e3aaa/file'
IMAGE_STR = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII="

def inference(model_id, prompt):
    search_config = copy.deepcopy(SEARCH_CONFIG)
    search_config["prompt"] = prompt
    payload = {
        "headers": {
          "content-type": "application/json",
          "accept": "application/json",
        },
        "body": json.dump(search_config),
        "method": "POST",
    }
    print("querying sd")
    response = requests.post(url=sd_url, json=payload)
    r = response.json()
    print("got result")
    return r["images"]

def upload_result_to_ipfs(result, file_name, bucket):
    """
    Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # Upload the file
    s3 = boto3.resource(
        's3', 
        aws_access_key_id=CHAIN_SAFE_S3_ID, 
        aws_secret_access_key=CHAIN_SAFE_S3_KEY,
        endpoint_url=CHAIN_SAFE_ENDPOINT)
    try:
        obj = s3.Object(bucket,file_name)
        obj.put(Body=base64.b64decode(result))

    except Exception as e:
        print('ChainSafe error!')
        logging.error(e)
        return ''
    
    data = {"path": file_name}
    headers = {"Authorization" : "Bearer " + CHAIN_SAFE_API_KEY}
    try:
        response = requests.post(CHAIN_SAFE_API, json=data, headers=headers)
        response_dict = json.loads(response.text)
        cid = response_dict["content"]["cid"]
    except Exception as e:
        print('unable to get result cid')
        logging.error(e)
    print(f'cid: {cid}')
    return cid


def submit_result(self, cid:str, job_id:str):
    try:
        self._contract.submitJob(cid,job_id, {'from': self._account})
    except Exception as e:
        print(e)




# define function to handle events and print to the console
def handle_event(event):
    job_id = event.args.jobId
    print(f"received job {job_id} start inference")
    # initialize the chain id, we need it to build the transaction for replay protection
    # Call your function
    result_img = inference(1, event.args.prompt)
    filename = str(job_id) + "_" + event.args.workerAddress
    cid = upload_result_to_ipfs(result_img, filename, CHAIN_SAFE_BUCKET_NAME)
    # Initialize address nonce
    nonce = web3.eth.get_transaction_count(caller)
    call_function = contract.functions.submitJob(cid, job_id).build_transaction({"chainId": Chain_id, "gasPrice": web3.eth.gas_price, "from": caller, "nonce": nonce})
    # Sign transaction
    signed_tx = web3.eth.account.sign_transaction(call_function, private_key=private_key)
    # Send transaction
    send_tx = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Wait for transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(send_tx)
    print(tx_receipt) # Optional


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    event_filter = contract.events.NewJobCreated.create_filter(fromBlock='latest')
    #block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 0.1)))
    finally:
        # close loop to free up system resources
        loop.close()


if __name__ == "__main__":
    main()