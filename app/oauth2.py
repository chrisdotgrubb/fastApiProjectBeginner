from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = 'longsecretkey'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
	to_encode = data.copy()
	expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({'exp': expire})
	return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	

def verify_access_token(token: str, credentials_exception):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		user_id: str = payload.get('user_id')
		if user_id is None:
			raise credentials_exception
		token_data = TokenData(id=user_id)
	except JWTError:
		raise credentials_exception
	return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
	credentials_exception = HTTPException(status_code=401, detail='Invalid Credentials', headers={'WWW-Authenticate': 'Bearer'})
	return verify_access_token(token, credentials_exception)
	