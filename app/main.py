from fastapi import FastAPI


from .routers import identity, scan

app = FastAPI()

app.include_router(identity.router)
app.include_router(scan.router)