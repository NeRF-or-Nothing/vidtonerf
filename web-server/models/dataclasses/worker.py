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

@dataclass
class Worker:
    id: Optional[str] = None
    api_key: Optional[str] = None
    owner_id: Optional[str] = None
    type: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Worker':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("_id"))
        api_key = from_union([from_str, from_none], obj.get("api_key"))
        owner_id = from_union([from_str, from_none], obj.get("owner_id"))
        type = from_union([from_str, from_none], obj.get("type"))
        return Worker(id, api_key, owner_id, type)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["_id"] = from_union([from_str, from_none], self.id)
        if self.api_key is not None:
            result["api_key"] = from_union([from_str, from_none], self.api_key)
        if self.owner_id is not None:
            result["owner_id"] = from_union([from_str, from_none], self.owner_id)
        if self.type is not None:
            result["type"] = from_union([from_str, from_none], self.type)
        return result


def worker_from_dict(s: Any) -> Worker:
    return Worker.from_dict(s)


def worker_to_dict(x: Worker) -> Any:
    return to_class(Worker, x)
