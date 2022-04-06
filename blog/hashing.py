from passlib.context import CryptContext

PWD_CXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    @classmethod
    def bcrypt(cls, password: str):
        return PWD_CXT.hash(password)
