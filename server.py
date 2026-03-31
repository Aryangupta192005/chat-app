import asyncio
import websockets
import os

clients = set()

async def handler(websocket):
    clients.add(websocket)
    print("Client connected")

    try:
        async for message in websocket:
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except Exception as e:
        print("Error:", e)
    finally:
        clients.remove(websocket)
        print("Client disconnected")

async def main():
    port = int(os.environ.get("PORT", 8080))

    server = await websockets.serve(
        handler,
        "0.0.0.0",
        port
    )

    print(f"Server running on port {port}")
    await server.wait_closed()

asyncio.run(main())
