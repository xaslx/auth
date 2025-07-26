from passlib.context import CryptContext


pwd_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')


class HashingService:
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)
