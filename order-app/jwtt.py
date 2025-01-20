import jwt

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjQsImV4cCI6MTczNjc4MzcwOX0.ks_lAhVe9-e-ZVJKwu1piPDOYqMt7jdgQUksXKwYlHw"

decoded_token = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])

print(decoded_token)
