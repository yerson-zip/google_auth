from argon2 import PasswordHasher

ph = PasswordHasher()


def password_hash(plane_text:str)->str:
    return ph.hash(plane_text)

def hash_validate(hash_password:str, password:str)->bool:
    return ph.verify(hash_password,password)


