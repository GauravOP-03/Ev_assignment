from fastapi import FastAPI
from routes import ops, client,auth
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(ops.router, prefix="/ops", tags=["Ops"])
app.include_router(client.router, prefix="/client", tags=["Client"])