from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os
import uuid
import datetime

app = FastAPI(title="PT WebApp - Backend (dev skeleton)")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
mongo = AsyncIOMotorClient(MONGO_URI)
db = mongo.pt_webapp

class RunRequest(BaseModel):
    PT_NAME: str
    ENV_TYPE: str  # 'k8' or 'vm'
    POD_COUNT: int = 1
    THREAD_GROUPS: list
    GAP_BETWEEN_ITERATION: int = 0

@app.on_event("startup")
async def startup_event():
    # ensure collection and indexes if needed
    await db.runs.create_index("run_id")

@app.get("/health")
async def health():
    return {"status": "ok", "time": datetime.datetime.utcnow().isoformat()}

@app.post("/api/runs")
async def create_run(payload: RunRequest):
    run_id = str(uuid.uuid4())
    doc = {
        "run_id": run_id,
        "payload": payload.dict(),
        "status": "PENDING",
        "created_at": datetime.datetime.utcnow()
    }
    await db.runs.insert_one(doc)
    # NOTE: Actual k8s job creation will be implemented in Step 3
    return {"run_id": run_id, "status": "PENDING"}
