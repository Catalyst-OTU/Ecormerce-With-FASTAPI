from tortoise import Model, fields
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator
from sqlalchemy import Column,Integer,Boolean,Text,String,ForeignKey,Double



class User(Model):
    __tablename__='user'
    id=fields.IntField(pk=True, index=True)
    username=fields.CharField(max_length=100, null=True, unique=True)
    email=fields.CharField(max_length=100, null=True, unique=True)
    password=fields.CharField(max_length=100, null=True)
    is_verified=fields.BooleanField(default=False)
    join_date=fields.DatetimeField(default=datetime.utcnow)




class Business(Model):
    __tablename__='business'
    id=fields.IntField(pk=True, index=True)
    business_name=fields.CharField(max_length=100, null=True)
    city=fields.CharField(max_length=100, null=True)
    region=fields.CharField(max_length=100, null=True)
    business_description=fields.TextField(null=True)
    logo=fields.CharField(max_length=100, null=True, default = "default.jpg")
    owner=fields.ForeignKeyField("models.User", related_name="business")




class Product(Model):
    __tablename__='product'
    id=fields.IntField(pk=True, index=True)
    name=fields.CharField(max_length=100, null=True, index=True)
    category=fields.CharField(max_length=100, null=True)
    orginal_price=fields.DecimalField(max_digits=12, decimal_places=2)
    new_price=fields.DecimalField(max_digits=12, decimal_places=2)
    percentage_discount=fields.IntField()
    offer_expiration_date=fields.DateField(default=datetime.utcnow)
    product_image=fields.CharField(max_length=100, default = "productDefault.jpg")
    business=fields.ForeignKeyField("models.Business", related_name="products")



user_pydantic = pydantic_model_creator(User, name = "User", exclude=("is_verified"))
user_pydanticIn = pydantic_model_creator(User, name = "UserIn", exclude_readonly=True, exclude=("is_verified", "join_date"))
user_pydanticOut = pydantic_model_creator(User, name = "UserOut", exclude=("password", ))

business_pydantic = pydantic_model_creator(Business, name = "Business")
business_pydanticIn = pydantic_model_creator(Business, name = "BusinessIn", exclude_readonly=True)

product_pydantic = pydantic_model_creator(Product, name = "Product")
product_pydanticIn = pydantic_model_creator(Product, name = "ProductIn", exclude=("percentage_discount", "id"))