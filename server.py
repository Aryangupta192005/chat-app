from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import os

app = FastAPI()
clients = []

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    print("Client connected")

    try:
        while True:
            data = await websocket.receive_text()
            for client in clients:
                if client != websocket:
                    await client.send_text(data)
    except WebSocketDisconnect:
        clients.remove(websocket)
        print("Client disconnected")
