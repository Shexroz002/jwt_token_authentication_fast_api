# app/auth.py

from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.schemas.user import DataToken, ResponseToken
from app.models.user import User, Token
from app.utils.auth_need_functions import pwd_context
from app.utils.credentials_exception import unauthorized_exception

# SECRET_KEY
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM
ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# oauth2_scheme for OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


# get_db function to get the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def verify_token_access(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = DataToken(id=id)
    except JWTError as e:
        raise credentials_exception

    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = unauthorized_exception()

    token = verify_token_access(token, credentials_exception)

    user = db.query(User).filter(User.id == token.id).first()

    return user


async def verify_password(non_hashed_pass, hashed_pass):
    return pwd_context.verify(non_hashed_pass, hashed_pass)


async def get_token(user_id: str, db: Session = Depends(get_db)) -> str:
    token = db.query(Token).filter(Token.user == user_id).first()
    return token.token if token else ''


async def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    return user


async def registered_user(username: str, password: str, db: Session = Depends(get_db)):
    user = await get_user(username, db=db)
    if not user:
        return False
    is_verify = await verify_password(password, user.password)
    if not is_verify:
        return False

    return user
