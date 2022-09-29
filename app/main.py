from fastapi import FastAPI
from fastapi_pagination import add_pagination

from .routers import identity, scan, index


tags = [
    {'name': 'identity', 'description': 'Identity endpoints'},
    {'name': 'scan', 'description': 'Scan endpoints'},
    {'name': 'index', 'description': 'Summary'}
]

app = FastAPI(openapi_tags=tags)

app.include_router(identity.router)
app.include_router(scan.router)
app.include_router(index.router)

add_pagination(app)