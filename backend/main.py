from contextlib import asynccontextmanager
import os

from fastapi import FastAPI, HTTPException
from temporalio.client import Client

from backend.models import PolicyRequest, PolicyResponse

from backend.models import PolicyResponse
from backend.workflows import PolicyWorkflow


temporal_client: Client | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global temporal_client

    temporal_address = os.getenv(
        "TEMPORAL_ADDRESS",
        "localhost:7233"
    )

    print(f"Connecting to Temporal at: {temporal_address}")

    temporal_client = await Client.connect(
        temporal_address
    )

    print("Temporal client connected.")

    yield

    # Shutdown
    temporal_client = None

    print("Temporal client disconnected.")


app = FastAPI(
    title="Policy API",
    lifespan=lifespan
)


def get_temporal_client() -> Client:
    if temporal_client is None:
        raise RuntimeError(
            "Temporal client has not been initialized."
        )

    return temporal_client

@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


@app.post(
    "/api/policies",
    response_model=PolicyResponse,
    status_code=202
)
async def create_policy(request: PolicyRequest):

    # Get Temporal SDK client
    client = get_temporal_client()

    workflow_id = f"policy-{request.policy_id}"

    try:

        # Client starts the workflow
        await client.start_workflow(
            PolicyWorkflow.run,
            args=[
                    request.policy_id,
                    request.customer_id,
                    request.coverage_amount
                ],
            id=workflow_id,
            task_queue="policy-task-queue"
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )

    return PolicyResponse(
        workflow_id=workflow_id,
        status="STARTED"
    )

@app.get(
    "/api/policies/{policy_id}/status"
)
async def get_policy_status(
    policy_id: str
):

    client =  get_temporal_client()

    workflow_id = f"policy-{policy_id}"

    workflow_handle = client.get_workflow_handle(
        workflow_id
    )

    try:

        description = (
            await workflow_handle.describe()
        )

        return {
            "workflow_id": workflow_id,
            # "status": str(
            #     description.status
            # ),
            "status": description.status.name,
        }

    except Exception as ex:

        raise HTTPException(
            status_code=404,
            detail=str(ex),
        )