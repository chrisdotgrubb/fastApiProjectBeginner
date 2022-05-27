from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class PostIn(BaseModel):
	title: str
	content: str
	is_published: bool = True
	
	class Config:
		orm_mode = True
		schema_extra = {
			"example": {
				"title": "Title of the post",
				"content": "Content of the post",
				"is_published": True,
			}
		}


class PostCreate(PostIn):
	pass


class PostUpdate(PostIn):
	is_published: bool


class PostOut(BaseModel):
	id: int
	title: str
	content: str
	is_published: bool
	created_at: datetime
	
	class Config:
		orm_mode = True
		schema_extra = {
			"example": {
				"id": 1,
				"title": "Title of the post",
				"content": "Content of the post",
				"is_published": True,
				"created_at": datetime.now(),
			}
		}


class UserBase(BaseModel):
	pass


class UserCreate(UserBase):
	email: EmailStr
	password: str


class UserOut(BaseModel):
	id: str
	email: EmailStr
	created_at: datetime
	
	class Config:
		orm_mode = True
		schema_extra = {
			"example": {
				"id": 1,
				"email": "your@email.com",
				"created_at": datetime.now(),
			}
		}


class UserLogin(BaseModel):
	email: EmailStr
	password: str


class Token(BaseModel):
	token: str
	token_type: str


class TokenData(BaseModel):
	id: Optional[str] = None
