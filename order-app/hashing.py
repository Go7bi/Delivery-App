from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrpt(password : str):
        return pwd_context.hash(password)
    def verify(hassing_password,plain_password):
        return pwd_context.verify(plain_password,hassing_password)
    
