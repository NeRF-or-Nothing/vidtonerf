from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast

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

# api_key owner
@dataclass
class User:
    username: Optional[str] = None
    password: Optional[str] = None
    _id: Optional[str] = None
    api_key: Optional[str] = None
    scenes: Optional[List[str]] = None
    workers_owned: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        username = from_union([from_str, from_none], obj.get("username"))
        password = from_union([from_str, from_none], obj.get("password"))
        _id = from_union([from_str, from_none], obj.get("_id"))
        api_key = from_union([from_str, from_none], obj.get("api_key"))
        scenes = from_union([lambda x: from_list(from_str, x), from_none], obj.get("scenes"))
        workers_owned = from_union([lambda x: from_list(from_str, x), from_none], obj.get("workers_owned"))
        return User(username, password, _id, api_key, scenes, workers_owned)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.username is not None:
            result["username"] = from_union([from_str, from_none], self.username)
        if self.password is not None:
            result["password"] = from_union([from_str, from_none], self.password)
        if self._id is not None:
            result["_id"] = from_union([from_str, from_none], self._id)
        if self.api_key is not None:
            result["api_key"] = from_union([from_str, from_none], self.api_key)
        if self.scenes is not None:
            result["scenes"] = from_union([lambda x: from_list(from_str, x), from_none], self.scenes)
        if self.workers_owned is not None:
            result["workers_owned"] = from_union([lambda x: from_list(from_str, x), from_none], self.workers_owned)

        return result


def user_from_dict(s: Any) -> User:
    return User.from_dict(s)


def user_to_dict(x: User) -> Any:
    return to_class(User, x)

