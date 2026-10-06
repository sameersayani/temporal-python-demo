from contextlib import asynccontextmanager
from fastapi import FastAPI
from temporalio.client import Client
import os

temporal_client: Client 

@asynccontextmanager
async def lifespan(app: FastAPI):
    global temporal_client

    temporal_client = await Client.connect(
        os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
    )
    yield

    temporal_client = None


app = FastAPI(
    title="Policy API",
    lifespan=lifespan
)

async def get_temporal_client() -> Client:
    return temporal_client