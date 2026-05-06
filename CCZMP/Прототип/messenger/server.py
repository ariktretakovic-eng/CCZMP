#!/usr/bin/env python3
import asyncio
import websockets
import json
from datetime import datetime

# Храним все активные соединения
connected_clients = set()
client_names = {}  # websocket -> nickname

async def broadcast(message, exclude=None):
    """Отправить сообщение всем подключённым клиентам, кроме exclude"""
    if connected_clients:
        await asyncio.wait([client.send(message) for client in connected_clients if client != exclude])

async def handler(websocket):
    # Регистрация нового клиента
    connected_clients.add(websocket)
    # Запрашиваем имя
    await websocket.send(json.dumps({"type": "system", "text": "Добро пожаловать в CCZMP Messenger. Введите ваше имя:"}))
    try:
        name_msg = await websocket.recv()
        name_data = json.loads(name_msg)
        nickname = name_data.get("name", "Аноним")
        client_names[websocket] = nickname
        await broadcast(json.dumps({"type": "system", "text": f"{nickname} присоединился к чату", "time": datetime.now().strftime("%H:%M:%S")}))
        
        # Основной цикл приёма сообщений
        async for message in websocket:
            data = json.loads(message)
            if data.get("type") == "message":
                text = data.get("text", "")
                sender = client_names.get(websocket, "Unknown")
                # Отправляем всем (включая отправителя, чтобы он видел своё сообщение)
                await broadcast(json.dumps({
                    "type": "message",
                    "sender": sender,
                    "text": text,
                    "time": datetime.now().strftime("%H:%M:%S")
                }))
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        # Клиент отключился
        connected_clients.remove(websocket)
        nickname = client_names.pop(websocket, "Аноним")
        await broadcast(json.dumps({"type": "system", "text": f"{nickname} покинул чат", "time": datetime.now().strftime("%H:%M:%S")}))

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Сервер CCZMP Messenger запущен на порту 8765")
        print("Подключайтесь через WebSocket: ws://localhost:8765 или ws://<ваш IP>:8765")
        await asyncio.Future()  # бесконечно

if __name__ == "__main__":
    asyncio.run(main())