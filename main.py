from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
	title: str
	content: str
	published: bool = True
	rating: Optional[int] = None


my_posts = [
	{
		'title': 'title of post 1',
		'content': 'content post 1',
		'published': True,
		'rating': 3,
		'id': 1
	},
	{
		'title': 'title of post 2',
		'content': 'content post 2',
		'published': True,
		'rating': 4,
		'id': 2
	}]


@app.get('/')
async def root():
	return {'message': 'Hello World'}


@app.get('/posts/')
def get_posts():
	context = {
		'data': my_posts
	}
	return context


@app.post('/posts/')
def post_create(post: Post):
	new_post = post.dict()
	new_post['id'] = len(my_posts) + 1
	my_posts.append(new_post)
	context = {
		'data': new_post
	}
	return context
