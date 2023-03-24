import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import *
from user import user_router

# from routes.api import router as api_router

app = FastAPI()



app.include_router(user_router)




# @app.get("/")
# def index():
#     return {"message": "Hello, world!"}





origins = ["http://localhost:8008"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



register_tortoise(
    app,
    db_url= "mysql://root:@localhost:3306/fastapi_ecormerce?charset=utf8",
    modules= {"models" : ["models"]},
    generate_schemas= True,
    add_exception_handlers= True
)
    

# app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8008, log_level="info", reload = True)
    print("running")