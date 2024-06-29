from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import CreateUser, UserOutput
from app.models.database import SessionLocal
from app.models.user import User, Token
from app.utils.auth_need_functions import hash_pass
from app.utils.authentication import create_access_token, get_token, registered_user
from app.utils.credentials_exception import login_exception

auth = APIRouter(
    prefix="/auth",
    tags=["BLOGS"],
    responses={404: {"description": "Not found"}},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auth.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserOutput)
def create_users(user: CreateUser, db: Session = Depends(get_db)):
    # Hash The Password
    hashed_pass = hash_pass(user.password)
    user.password = hashed_pass
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@auth.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Check if user is registered
    user = await registered_user(form_data.username, form_data.password, db=db)
    # If user is not registered, raise an exception as the user is not registered
    if not user:
        raise login_exception()
    # Check if the user has a token
    token_data = await get_token(user.id, db=db)
    # If the user does not have a token, create a new token
    if not token_data:
        # Create a new token
        access_token = await create_access_token(
            data={"user_id": user.id}
        )
        expire = datetime.utcnow() + timedelta(days=5)
        new_token = Token(token=access_token, user=user.id, token_data=expire)
        db.add(new_token)
        db.commit()
        db.refresh(new_token)
        return {"access_token": new_token.token, "token_type": "bearer", 'user_id': user.id, }

    return {"access_token": token_data, "token_type": "bearer", 'user_id': user.id}
