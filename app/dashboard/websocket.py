import json
import asyncio
from fastapi import WebSocket
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class WebSocketManager:
    """Manage WebSocket connections and broadcasting for real-time updates."""
    
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []
        self.message_queue: asyncio.Queue = asyncio.Queue()

    async def connect(self, websocket: WebSocket) -> None:
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket) -> None:
        """Remove a disconnected WebSocket."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: Dict[str, Any]) -> None:
        """Broadcast a message to all connected clients."""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

    async def send_personal(self, websocket: WebSocket, message: Dict[str, Any]) -> None:
        """Send a message to a specific connection."""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)

    def get_connection_count(self) -> int:
        """Get number of active connections."""
        return len(self.active_connections)

    async def send_benchmark_update(self, benchmark_id: str, status: str, metrics: Dict[str, Any]) -> None:
        """Send a benchmark status update to all connected clients."""
        message = {
            "type": "benchmark_update",
            "benchmark_id": benchmark_id,
            "status": status,
            "metrics": metrics,
        }
        await self.broadcast(message)
