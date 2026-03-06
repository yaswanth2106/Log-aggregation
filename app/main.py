from fastapi import FastAPI,WebSocket

from .database import engine, Base
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from typing import List
from prometheus_fastapi_instrumentator import Instrumentator
import asyncio




active_connections: List[WebSocket] = []

from .routes import router





limiter = Limiter(key_func=get_remote_address)


Base.metadata.create_all(bind=engine)


app = FastAPI(title="Log Aggregation Service")
app.include_router(router)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
Instrumentator().instrument(app).expose(app)


@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            await websocket.send_text("connected")
            await asyncio.sleep(10)
    except:
        active_connections.remove(websocket)

@app.get("/get")
def root():
    return {"message": "Log Aggregation System Running"}
