from time import sleep
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
	title: str
	content: str
	published: bool = True
	rating: Optional[int] = None
	is_active: bool = True

host = 'localhost'
db = 'fastAPIBeginner'
user = 'postgres'
pw = 'password'

while True:
	try:
		conn = psycopg2.connect(host=host, database=db, user=user, password=pw, cursor_factory=RealDictCursor)
		cursor = conn.cursor()
		print('db connection successful')
		break
	except psycopg2.OperationalError as error:
		print('db connection failed')
		print(error)
		sleep(3)
	
my_posts = [
	{
		'title': 'title of post 1',
		'content': 'content post 1',
		'published': True,
		'rating': 3,
		'id': 1,
		'is_active': True
	},
	{
		'title': 'title of post 2',
		'content': 'content post 2',
		'published': True,
		'rating': 4,
		'id': 2,
		'is_active': True
	}]


@app.get('/')
async def root():
	return {'message': 'Hello World'}


@app.get('/posts/')
def get_posts():
	cursor.execute('SELECT * FROM posts')
	posts = cursor.fetchall()
	context = {
		'data': posts
	}
	return context


@app.post('/posts/', status_code=201)
def create_post(post: Post):
	new_post = post.dict()
	new_post['id'] = len(my_posts) + 1
	my_posts.append(new_post)
	context = {
		'data': new_post
	}
	return context

@app.get('/posts/{pk}/')
def get_post(pk: int, response: Response):
	data = {}
	try:
		data['post'] = my_posts[pk - 1]
		if not data['post']['is_active']:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {pk} was not found.')
	except IndexError:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {pk} was not found.')
	context = {
		'data': data
	}
	return context
	
@app.delete('/posts/{pk}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(pk: int):
	try:
		my_posts[pk - 1]['is_active'] = False
	except IndexError:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {pk} was not found.')
	return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{pk}/')
def update_post(pk: int, post: Post):
	try:
		my_posts[pk - 1] = post.dict()
		item = my_posts[pk - 1]
		item['id'] = pk
	except IndexError:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {pk} was not found.')
	return {'data': item}
	
