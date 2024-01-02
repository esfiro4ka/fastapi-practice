from passlib.context import CryptContext

crypt_ctx = CryptContext(schemes=['bcrypt'])


def encode_password(password: str):
    return crypt_ctx.hash(password)


def verify_password(password: str, encoded_password: str):
    return crypt_ctx.verify(password, encoded_password)
