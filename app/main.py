from fastapi import FastAPI

from .api.v1.secrets import router

from .db import client


app = FastAPI()


@app.on_event("shutdown")
async def shutdown_event():
    client.close()

app.include_router(router)