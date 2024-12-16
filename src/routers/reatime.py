from fastapi import APIRouter, WebSocket, WebSocketDisconnect, BackgroundTasks
from ..models.course_model import Course
import asyncio
router = APIRouter(
    prefix="/real_time",
    tags=["Realtime"],
)

async def send_periodic_message(websocket: WebSocket):
    try:
        while True:
            await websocket.send_json({
                "message": "This is a periodic update"
            })
            await asyncio.sleep(10)  # Adjust the interval as needed
    except WebSocketDisconnect:
        pass  # Handle disconnection

@router.websocket("/seats")
async def websocket_endpoint(websocket: WebSocket, background_tasks: BackgroundTasks):
    global active_websocket
    await websocket.accept()
    active_websocket = websocket
    print("Client connected")

    # Send initial connection data
    await websocket.send_json(Course())
    
    # Add the background task to send periodic messages
    background_tasks.add_task(send_periodic_message, websocket)

    try:
        while True:
            # Continuously listen for messages from the client
            message = await websocket.receive_json()
            sample_message = {
                "from": "client",
                "message": "ask_update"
            }
            print(f"Received message: {message}")
    except WebSocketDisconnect:
        active_websocket = None
        print("Client disconnected")
