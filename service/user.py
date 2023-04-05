from dao.user import UserDAO
import hashlib
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
import hmac
import base64

class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_d):
        user_d["password"] = self.get_hash(user_d["password"])
        return self.dao.create(user_d)

    def update(self, user_d):
        result = self.get_one(user_d.get("id"))
        if user_d.get("email"):
            result.email = user_d.get("email")
        if user_d.get("password"):
            result.password = user_d.get("password")
        if user_d.get("favorite_genre"):
            result.favorite_genre = user_d.get("favorite_genre")
        if user_d.get("name"):
            result.name = user_d.get("name")
        if user_d.get("surname"):
            result.surname = user_d.get("surname")
        return self.dao.update(result)

    def delete(self, uid):
        return self.dao.delete(uid)

    def get_hash(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_digest)

    def get_by_email(self, email):
        return self.dao.get_by_email(email)

    def compare_password(self, password_hash, other_password):
        decoded_digist = base64.b64decode(password_hash)

        hash_digest = hashlib.pbkdf2_hmac(
            "sha256",
            other_password.encode("utf-8"),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return hmac.compare_digest(decoded_digist, hash_digest)
