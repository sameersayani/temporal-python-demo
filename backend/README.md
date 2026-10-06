                       ┌──────────────┐
                       │    React     │
                       └──────┬───────┘
                              │
                         HTTP/HTTPS
                              │
                              ▼
                    ┌──────────────────┐
                    │     FastAPI      │
                    │                  │
                    │ POST /policies   │
                    │ GET /status      │
                    │ GET /result      │
                    └────────┬─────────┘
                             │
                       Temporal Client
                             │
                             ▼
                  ┌──────────────────────┐
                  │   Temporal Service   │
                  │                      │
                  │ Workflow History     │
                  │ Task Queues          │
                  │ Retry/Timers         │
                  └──────────┬───────────┘
                             │
                   policy-task-queue
                             │
                             ▼
                  ┌──────────────────────┐
                  │   Python Worker      │
                  │                      │
                  │ PolicyWorkflow       │
                  └──────────┬───────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        Validate         Calculate        Save
        Activity         Activity        Activity
                                           │
                                           ▼
                                      PostgreSQL

                             │
                             ▼
                       Notification
                         Activity

Important point:
Activity
   │
   ├── Database
   ├── REST API
   ├── Email
   ├── AWS
   └── External systems

How it works:
FastAPI
   │
   │
   │ get_temporal_client()
   ▼
Temporal SDK Client
   │
   │ gRPC
   ▼
Temporal Server
   │
   │ Task Queue
   ▼
Temporal Worker
   │
   ├── Workflow
   │
   └── Activities

How to run Temporal locally?
1. Install Temporal CLI, like for windows I installed: temporal_cli_1.9.1_windows_amd64
2. Run in CMD: temporal server start-dev, this will run the tempral server locally
3. You can see localhost:7233 and  http://localhost:8233 running
4. You can see Temporal UI on port 8233
5. In VS Code or your other IDE, open a new terminal and run python -m backend.worker. This will run Temporal worker
6. Keep both Temporal Server and Temporal Worker running
7. Now open another terminal and run uvicorn backend.main:app. This will run the API at port 8000
8. Open http://127.0.0.1:8000/docs
9. Check healthcheck
10. Hit post endpoint and see Temporal UI. You will notice new workflow Id for each hit on Post endpoint you did.
11. Clicking on workflow id will take you to worker ran and also show you task queue where each task gets executed.