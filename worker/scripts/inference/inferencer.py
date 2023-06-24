from brownie import Contract
from brownie.network.account import Account
import requests

import logging
import boto3
from botocore.exceptions import ClientError
import base64
import os
import json

CHAIN_SAFE_KEY_ID = 'MHHARRNNQMSRDZECLSBN'
CHAIN_SAFE_API_KEY = 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODc1NzE2NjYsImNuZiI6eyJqa3UiOiIvY2VydHMiLCJraWQiOiI5aHE4bnlVUWdMb29ER2l6VnI5SEJtOFIxVEwxS0JKSFlNRUtTRXh4eGtLcCJ9LCJ0eXBlIjoiYXBpX3NlY3JldCIsImlkIjoxMjk0MCwidXVpZCI6ImI5NWE3ZGJkLTViOWEtNGYwYy1hZjA3LTU3YWFlNjE3YmQ2ZCIsInBlcm0iOnsiYmlsbGluZyI6IioiLCJzZWFyY2giOiIqIiwic3RvcmFnZSI6IioiLCJ1c2VyIjoiKiJ9LCJhcGlfa2V5IjoiTUhIQVJSTk5RTVNSRFpFQ0xTQk4iLCJzZXJ2aWNlIjoic3RvcmFnZSIsInByb3ZpZGVyIjoiIn0.Te0Qu_vx1RVBKFHOVeGsI62QwBGC7fYWvItPK-QvxQGBbRDMD-WXWSwgKj00YXi6o315FssiePXovPTzqzry1g'
CHAIN_SAFE_ENDPOINT = 'https://buckets.chainsafe.io'
CHAIN_SAFE_BUCKET_NAME = 'Artifex'

CHAIN_SAFE_S3_KEY = 'R2W8Tg8p0ZhYkDf4qrZed8jbA4T6obfeICQfQyfu'
CHAIN_SAFE_S3_ID = 'YJCJAJFUGJVKXTMHYDTF'

CHAIN_SAFE_API= 'https://api.chainsafe.io/api/v1/bucket/d65358b3-ea8d-4c77-b529-f9ba403e3aaa/file'


IMAGE_STR = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII="

class JobInferencer():
    def __init__(self) -> None:
        self._account = None
        self._contract = None

    def setup(self, account:Account, contract: Contract):
        self._account = account
        self._contract = contract

    def handle_new_job(self,job_id, worker_address,model_id,prompt):
        if(worker_address != self._account.address):
            print(f'Current worker: {self._account.address}, Skip')
            pass
        print(f'Current worker: {self._account.address}, Pick up the job')
        result = self.inference(model_id,prompt)
        file_name : str = str(job_id) + '_' + worker_address
        cid = self.upload_result_to_ipfs(result,file_name,CHAIN_SAFE_BUCKET_NAME)
        self.submit_result(cid,job_id)
        

    def inference(self, model_id, prompt):
        return IMAGE_STR

    ##Use ChainSafe S3 like API to upload result to IPFS
    def upload_result_to_ipfs(self, result, file_name, bucket):
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
    
