from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import time
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import asyncio
from .routers import video, seats, survey, status, picture, auth
import json

# List of clients (queues for SSE connections)
clients: List[asyncio.Queue] = []

# Hold the reference to the main event loop
loop: asyncio.AbstractEventLoop = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global loop
    loop = asyncio.get_event_loop()  # Get the main event loop at the start
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_event, 'interval', seconds=5000)  # Trigger every 5 seconds
    scheduler.start()
    yield


# Initialize FastAPI app with lifespan (context manager)
app = FastAPI(lifespan=lifespan)

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware to measure request processing time
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    print(f"Request took {time.time() - start_time} sec")
    return response


# Function to send events to all connected clients
async def send_event_to_clients(message: dict):
    """Send a message to all connected clients via SSE."""
    for client in clients:
        await client.put(message)


# Event stream function to keep the connection open and send data
async def event_stream():
    """Streaming data to connected clients (SSE)."""
    while True:
        client = asyncio.Queue()
        clients.append(client)
        
        try:
            while True:
                message = await client.get()
                yield f"data: {json.dumps(message)}\n\n"
                await asyncio.sleep(1)  # Small sleep to mimic the streaming
        except asyncio.CancelledError:
            clients.remove(client)  # Remove client if it disconnects


@app.get("/events")
async def sse_endpoint():
    """Endpoint for the client to connect via SSE."""
    return StreamingResponse(event_stream(), media_type="text/event-stream")


# APScheduler job function that triggers events
def scheduled_event():
    """Scheduled task that triggers an event periodically."""
    event_message = {
        "event": "Scheduled event",
        "timestamp": time.ctime()
    }
    
    # Use asyncio.run_coroutine_threadsafe to run the async function in the event loop
    asyncio.run_coroutine_threadsafe(send_event_to_clients(event_message), loop)


@app.post("/trigger_event")
async def trigger_event():
    """Trigger an event manually."""
    event_message = {
        "to": "client",
        "event": "Manual event triggered",
        "timestamp": time.ctime()
    }
    
    # Send the manual event to all connected clients
    asyncio.create_task(send_event_to_clients(event_message))
    return {"message": "Event triggered successfully!"}


app.include_router(video.router)
app.include_router(seats.router)
app.include_router(survey.router)
app.include_router(status.router)
app.include_router(picture.router)
app.include_router(auth.router)

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     global active_websocket
#     await websocket.accept()
#     active_websocket = websocket
#     print("client connected")
#     await websocket.send_json(
#         {
#             "device": "device.id",
#             "image": "teacher.id",
#             "teacher": "teacher.name",
#             "school": "teacher.school"
#         }
#     )
#     try:
#         while True:
#             message = await websocket.receive_text()
#     except WebSocketDisconnect:
#         active_websocket = None
#         print("Client disconnected")
