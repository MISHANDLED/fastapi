from passlib.context import CryptContext

pass_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")

def hashpass(password: str):
    return pass_context.hash(password)