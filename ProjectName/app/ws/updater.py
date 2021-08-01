import asyncio
from datetime import datetime

from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect
from websockets import exceptions

from ProjectName.app.main import app


@app.websocket("/ws")
async def websocket_endpoint_time(websocket: WebSocket):
    from .ConnectionManager import manager
    client_id = id(websocket).__int__()
    await manager.connect(websocket)
    try:
        await manager.send_personal_message(f"You joined the time update chat", websocket)
        await manager.broadcast(f"Client #{client_id} joined for time updates")
        while True:
            await manager.send_personal_message(f"Hey #{client_id}, its {datetime.now()}", websocket)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the time update chat")
    except exceptions.ConnectionClosedError:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} was forcefully closed")
    except exceptions.ConnectionClosedOK:
        manager.disconnect(websocket)
