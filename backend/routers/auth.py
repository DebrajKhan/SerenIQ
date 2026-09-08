from fastapi import APIRouter, HTTPException, status
from models.sign_in_models import LogInDataAuth
from models.sign_up_models import SignUpDataAuth
from databases.database import users_collection
from core.security import pwd_context, create_access_token

router = APIRouter(tags=["Authentication"])

@router.post("/sign-up")
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

        access_token = create_access_token(data={"sub":user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server error during registration: {e}"
        )


@router.post("/sign-in")
async def sign_in(user: LogInDataAuth):
    try:
        existing_user = await users_collection.find_one({"email": user.email})
        if existing_user:
            hashed_db_password = existing_user.get("password")
            if pwd_context.verify(user.password, hashed_db_password):
                
                access_token = create_access_token(data={"sub": user.email})
                print(f"User signed in successfully: {user.email}")
                
                return {"access_token": access_token, "token_type": "bearer"}
            
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Password did not match"
                )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{user.email} is not found!"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server error: {e}"
        )