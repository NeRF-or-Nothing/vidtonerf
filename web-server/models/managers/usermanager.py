from typing import Any, List, TypeVar, Callable, Type, cast
from pymongo import MongoClient
from uuid import uuid4
from ..dataclasses.user import User


# dataclasses generated with Quicktype https://github.com/quicktype/quicktype
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = scene_from_dict(json.loads(json_string))


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x

def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class UserManager:
    def __init__(self) -> None:
        # TODO: Host variable has to be changed whether run inside or outside of a docker container
        client = MongoClient(host="localhost", port=27017, username="admin", password="password123")
        self.db = client["nerfdb"]
        self.collection = self.db["users"]
        self.upsert = True

    def set_user(self, user: User):  # usernames and ids are forced to be unique, passwords are not
        key = {"username": user.username}
        doc = self.collection.find_one(key)
        if doc != None:
            # Two users assigned with same username
            return 1
        key = {"_id": user._id}
        doc = self.collection.find_one(key)
        if doc != None:
            raise Exception('Two users assigned with same ID!')
        user.password = str(hash(user.password))

        value = {"$set": user.to_dict()}
        self.collection.update_one(key, value, upsert=self.upsert)
        return 0

    def generate_user(self, username: str, password: str):
        _id = str(uuid4())
        user = User(username, password, _id)
        errorcode = self.set_user(user)
        if (errorcode != 0):
            return errorcode

        return user

    def get_user_by_id(self, _id: str) -> User:
        key = {"_id": _id}
        doc = self.collection.find_one(key)
        if doc:
            return User.from_dict(doc)
        else:
            return None

    def get_user_by_username(self, username: str) -> User:
        key = {"username": username}
        doc = self.collection.find_one(key)
        if doc:
            return User.from_dict(doc)
        else:
            return None
    # TODO: Write an overloaded function for finding users by username

    # def user_exists(self):
    # TODO: Write an overloaded function for finding if a user exists by username
