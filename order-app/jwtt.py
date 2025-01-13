import jwt

# Example JWT token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjQsImV4cCI6MTczNjc4MzcwOX0.ks_lAhVe9-e-ZVJKwu1piPDOYqMt7jdgQUksXKwYlHw"

# Decode token without signature verification (be careful, this is for debugging purposes)
decoded_token = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])

print(decoded_token)
