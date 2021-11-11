from passlib.context import CryptContext

pass_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")

def hashpass(password: str):
    return pass_context.hash(password)

def verifypass(plain_pass, hash_pass):
    return pass_context.verify(plain_pass, hash_pass)