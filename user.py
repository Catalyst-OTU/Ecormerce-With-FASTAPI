from fastapi import APIRouter, Request, HTTPException, status
from models import *
from authentication import *
from sendemail import *

#Signals
from tortoise.signals import post_save
from typing import List,Optional, Type
from tortoise import BaseDBAsyncClient


#RESPONSE CLASSES
from fastapi.responses import HTMLResponse

#TEMPLATES
from fastapi.templating import Jinja2Templates


user_router=APIRouter(
    prefix='/users',
    tags=['users']
)



@user_router.get('/getAllUsers')
async def get_users():
    response = await user_pydantic.from_queryset(User.all())
    return {"status": "ok", "data": response}



@user_router.get('/product')
async def get_product():
    response = await product_pydantic.from_queryset(Product.all())
    return {"status": "ok", "data": response}



@post_save(User)
async def create_business(
    sender: "Type[User]",
    instance: User,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str]
) -> None:
        
    if created:
        business_obj = await Business.create(
            business_name = instance.username, owner = instance
        )

        await business_pydantic.from_tortoise_orm(business_obj)
        # SEND EMAIL
        await send_email([instance.email], instance)





@user_router.post('/registerUser')
async def user_registration(user: user_pydanticIn):
    user_info = user.dict(exclude_unset=True)
    user_info["password"] = get_hashed_password(user_info["password"])
    user_obj = await User.create(**user_info)
    new_user= await user_pydantic.from_tortoise_orm(user_obj)
    return{
        "status" : "ok",
        "data" : f"You are welcome {new_user.username}, Please check your email to confirm your registration"
    }




templates = Jinja2Templates(directory="templates")

@user_router.get('/verification', response_class=HTMLResponse)
async def email_verification(request:Request, token:str):
    user = await verify_token(token)

    if user and not user.is_verified:
        user.is_verified = True
        await user.save()
        return templates.TemplateResponse("verification.html", 
                                          {"request":request, "username": user.username}
                                          )
    

    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details="Invalid token or token expired",
            headers={"WWW-Authentication": "Bearer"}
        )