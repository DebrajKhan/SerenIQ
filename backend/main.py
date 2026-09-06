from contextlib import asynccontextmanager
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from model import LogInData, LogInDataAuth, SignUpData,  SignUpDataAuth
from database import connected_to_mongoDB, terminate_mongoDB, users_collection


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

pwd_context = CryptContext(schemes=['bcrypt'], deprecated ='auto')

        
@app.post("/sign-in", response_model=LogInData)
async def sign_in(user:LogInDataAuth):
    try:
        existing_user = await users_collection.find_one({"email": user.email})
        if existing_user:
            hashed_db_password = existing_user.get("password")
            if  pwd_context.verify(user.password, hashed_db_password):
                return {"email" : user.email}
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail = "password did not match"
                )

        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail = f"{user.email} is not found!"
                )
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server error: {e}"
        )

@app.post("/sign-up", response_model=SignUpData)
async def sign_up(user:SignUpDataAuth):
    try:
        existing_user = await users_collection.find_one({"email" : user.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail = f"{user.email} already exists"
            )

        hashed_password = pwd_context.hash(user.password)

        user_data = user.model_dump()
        user_data["password"] = hashed_password

        await users_collection.insert_one(user_data)
        print(f"New user successfully registered: {user.email}")

        return user
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server error during registration: {e}"
        )

