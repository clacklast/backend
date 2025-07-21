from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import init_db
from app.router import router
from fluent import handler

fluent_host="192.168.100.77"
fluent_port=24224
app_name="bootcamp2-backend"
fluent_handler = handler.FluentHandler(app_name, host=fluent_host, port=fluent_port)
formatter = handler.FluentRecordFormatter({
    'job': app_name,
    'host': '%(hostname)s',
    'where': '%(module)s.%(funcName)s',
    'path': '%(path)s',
    'request': '%(request)s',
    'ip': '%(ip)s',
    'message': '%(message)s'
})
fluent_handler.setFormatter(formatter)

logger = logging.getLogger("fastapi")
logger.setLevel(logging.INFO)
logger.addHandler(fluent_handler)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def start_db():
    logger.info("Request a /", extra=g.log_extra)
    await init_db()

app.include_router(router, prefix="/api")

