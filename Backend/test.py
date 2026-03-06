from app.utils.jwt_handler import create_access_token

token = create_access_token("123456")

print(token)