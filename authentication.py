from passlib.context import CryptContext
import jwt
from dotenv import dotenv_values
from models import User
from fastapi.exceptions import HTTPException
from fastapi import status

config_credentials = dotenv_values(".env")


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_hashed_password(password):
    return pwd_context.hash(password)



async def verify_token(token: str):
    try:
        payload = jwt.decode(token, "e9b684988b11fc27d0f2e00bf7cfa45b6c4b97a2",algorithm=['HS256'])
        user = await User.id(id = payload.get('id'))

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details="Invalid token",
            headers={"WWW-Authentication": "Bearer"}
        )
    

    return user