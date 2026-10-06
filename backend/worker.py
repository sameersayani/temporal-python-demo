import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from .workflows import PolicyWorkflow

from .activities import (
    validate_policy,
    calculate_premium,
    save_policy,
    send_notification,
)


async def main():

    client = await Client.connect(
        "localhost:7233"
    )

    worker = Worker(
        client,

        task_queue="policy-task-queue",

        workflows=[
            PolicyWorkflow
        ],

        activities=[
            validate_policy,
            calculate_premium,
            save_policy,
            send_notification,
        ],
    )

    print(
        "Temporal Worker started..."
    )

    await worker.run()


if __name__ == "__main__":

    asyncio.run(main())