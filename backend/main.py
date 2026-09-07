from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from databases.database import connected_to_mongoDB, terminate_mongoDB
from routers import auth



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing server resources...")
    await connected_to_mongoDB()
    
    yield 

    print("Cleaning up server resources...")
    await terminate_mongoDB()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_headers = ["*"],
    allow_methods=["*"],
    allow_credentials=True
)

app.include_router(auth.router)



