import asyncio
from brownie import Contract, accounts
from .config import CONTRACT_ADDRESS, ACCOUNT_ALIAS
from .inference.inferencer import JobInferencer


inferencer = JobInferencer()

def main():
    # Contract instance
    contract = Contract(CONTRACT_ADDRESS)
    # Contract Account
    account = accounts.load(ACCOUNT_ALIAS)

    inferencer.setup(account, contract)
    
    # Event filters
    job_created_event = contract.events.NewJobCreated.createFilter(fromBlock='latest')
    job_submitted_event = contract.events.JobSubmited.createFilter(fromBlock='latest')
    # Mapping from event type to its filter
    
    event_filters = {
        'NewJobCreated': job_created_event,
        'JobSubmitted': job_submitted_event
    }

    # Mapping from event type to its handler
    event_handlers = {
        'NewJobCreated': handle_job_created_event,
        'JobSubmitted': handle_job_submitted_event
    }

    # Run the log loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(log_loop(event_filters, event_handlers, 2))
    finally:
        loop.close()

async def log_loop(event_filters, event_handlers, poll_interval):
    while True:
        for event_type, event_filter in event_filters.items():
            for event in event_filter.get_new_entries():
                await event_handlers[event_type](event)
        await asyncio.sleep(poll_interval)

async def handle_job_created_event(event):
    job_id = event["args"]["jobId"]
    worker_address = event["args"]["workerAddress"]
    model_id = event["args"]["modelId"]
    prompt = event["args"]["prompt"]
    print(f'New job created: {job_id}, assigned to worker {worker_address}')
    inferencer.handle_new_job(job_id,worker_address,model_id,prompt)

async def handle_job_submitted_event(event):
    job_id = event["args"]["jobId"]
    cid = event["args"]["resultCid"]
    print(f'Job submitted: {job_id}, cid: {cid}')


if __name__ == "__main__":
    main()
