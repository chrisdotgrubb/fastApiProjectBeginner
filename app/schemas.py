from datetime import datetime

from pydantic import BaseModel


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
