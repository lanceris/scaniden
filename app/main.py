from fastapi import FastAPI
from fastapi_pagination import add_pagination

from .routers import identity, scan


tags = [
    {'name': 'identity', 'description': 'Identity endpoints'},
    {'name': 'scan', 'description': 'Scan endpoints'}
]

app = FastAPI(openapi_tags=tags)

app.include_router(identity.router)
app.include_router(scan.router)

add_pagination(app)