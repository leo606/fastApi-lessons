from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str
    user_id = int


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    user = ShowUser

    class Config:
        orm_mode = True
