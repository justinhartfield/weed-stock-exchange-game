from typing import List, Dict
from fastapi import WebSocket
import json


class ConnectionManager:
    """Manages WebSocket connections for real-time updates."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept and store a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: Dict, websocket: WebSocket):
        """Send a message to a specific client."""
        await websocket.send_text(json.dumps(message))
    
    async def broadcast(self, message: Dict):
        """Broadcast a message to all connected clients."""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                disconnected.append(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)
    
    async def broadcast_price_update(self, strain_id: int, price: float, change_pct: float):
        """Broadcast a price update for a specific strain."""
        await self.broadcast({
            "type": "price_update",
            "strain_id": strain_id,
            "price": price,
            "change_pct": change_pct
        })
    
    async def broadcast_market_event(self, event: Dict):
        """Broadcast a market event."""
        await self.broadcast({
            "type": "market_event",
            "event": event
        })


# Global connection manager instance
manager = ConnectionManager()
