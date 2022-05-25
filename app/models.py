from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String, text, TIMESTAMP

from .database import Base


class Post(Base):
	__tablename__ = 'posts'
	
	id = Column(Integer, primary_key=True, nullable=False)
	title = Column(String, nullable=False)
	content = Column(String, nullable=False)
	is_published = Column(Boolean, server_default='true', nullable=False)
	created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



class PostIn(BaseModel):
	title: str
	content: str
	is_published: bool = True
