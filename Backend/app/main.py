from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.routers import auth_router, user_router, slot_router
from app.websocket.connection_manager import manager
from app.utils.room_storage import save_code, load_code
from app.utils.cleanup_rooms import cleanup_rooms

import asyncio


app = FastAPI()


# ---------------------------
# Register REST API Routers
# ---------------------------

app.include_router(auth_router.router, prefix="/api/auth")
app.include_router(user_router.router, prefix="/api/user")
app.include_router(slot_router.router, prefix="/api/slots")


# ---------------------------
# Root Endpoint
# ---------------------------

@app.get("/")
def home():
    return {"message": "Mock Interview Platform Backend Running 🚀"}


# ---------------------------
# WebSocket Interview Room
# ---------------------------

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):

    # connect user to room
    await manager.connect(websocket, room_id)

    # load previously saved code
    existing_code = load_code(room_id)

    await websocket.send_json({
        "type": "initial-code",
        "code": existing_code
    })

    try:
        while True:

            data = await websocket.receive_json()
            event_type = data.get("type")

            # ------------------
            # User joins room
            # ------------------
            if event_type == "join-room":

                await manager.broadcast(room_id, {
                    "type": "peer-connected"
                })


            # ------------------
            # WebRTC signaling
            # ------------------
            elif event_type == "signal":

                await manager.broadcast(room_id, {
                    "type": "signal",
                    "signalData": data.get("signalData")
                })


            # ------------------
            # Code collaboration
            # ------------------
            elif event_type == "code-change":

                code = data.get("code")

                # save latest code to file
                save_code(room_id, code)

                await manager.broadcast(room_id, {
                    "type": "code-change",
                    "code": code
                })

    except WebSocketDisconnect:

        manager.disconnect(websocket, room_id)
        print(f"User disconnected from room {room_id}")


# ---------------------------
# Room Cleanup Scheduler
# ---------------------------

async def cleanup_scheduler():

    while True:

        cleanup_rooms()

        # run every 1 hour
        await asyncio.sleep(3600)


@app.on_event("startup")
async def start_cleanup():

    asyncio.create_task(cleanup_scheduler())