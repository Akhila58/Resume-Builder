from pydantic import BaseModel

class SignUp(BaseModel):
    email : str
    username:str
    password:str
    
class Login(BaseModel):
    email:str
    password:str
    
class Token(BaseModel):
    access_token:str
    token_type:str