from fastapi import FastAPI
from server.routers import users
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(users.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
