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
	is_published: bool = True
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


@app.get('/')
async def root():
	return {'message': 'Hello World'}


@app.get('/posts/')
def get_posts():
	cursor.execute('SELECT * FROM posts')
	posts = cursor.fetchall()
	context = {
		'data': {'posts': posts}
	}
	return context


@app.post('/posts/', status_code=201)
def create_post(post: Post):
	cursor.execute(
		"""
		INSERT INTO posts(title, content, is_published, rating, is_active)
		VALUES (%s, %s, %s, %s, %s)
		RETURNING *
		""",
		vars=(post.title, post.content, post.is_published, post.rating, post.is_active))
	new_post = cursor.fetchone()
	conn.commit()
	context = {
		'data': {'post': new_post}
	}
	return context


@app.get('/posts/{pk}/')
def get_post(pk: int, response: Response):
	cursor.execute(
		"""
		SELECT *
		FROM posts
		WHERE id = %s
		AND is_published = true
		AND is_active = true
		""",
		vars=(pk,)
	)
	post = cursor.fetchone()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {pk} was not found.')
	context = {
		'data': {'post': post}
	}
	return context


@app.delete('/posts/{pk}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(pk: int):
	cursor.execute(
		"""
		DELETE
		FROM posts
		WHERE id = %s
		RETURNING *
		""",
		vars=(pk,)
	)
	post = cursor.fetchone()
	conn.commit()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {pk} was not found.')
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{pk}/')
def update_post(pk: int, post: Post):
	cursor.execute(
		"""
		UPDATE posts
		SET title = %s, content = %s, is_published = %s, rating = %s
		WHERE id = %s
		RETURNING *
		""",
		vars=(post.title, post.content, post.is_published, post.rating, pk)
	)
	updated = cursor.fetchone()
	conn.commit()
	if not updated:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {pk} was not found.')
	return {'data': {'post': updated}}
