from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast
from video import Video
from sfm import Sfm
from nerf import Nerf
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
class Scene:
    id: Optional[str] = None
    status: Optional[int] = None
    video: Optional[Video] = None
    sfm: Optional[Sfm] = None
    nerf: Optional[Nerf] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Scene':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        status = from_union([from_int, from_none], obj.get("status"))
        video = from_union([Video.from_dict, from_none], obj.get("video"))
        sfm = from_union([Sfm.from_dict, from_none], obj.get("sfm"))
        nerf = from_union([Nerf.from_dict, from_none], obj.get("nerf"))
        return Scene(id, status, video, sfm, nerf)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_str, from_none], self.id)
        result["status"] = from_union([from_int, from_none], self.status)
        result["video"] = from_union([lambda x: to_class(Video, x), from_none], self.video)
        result["sfm"] = from_union([lambda x: to_class(Sfm, x), from_none], self.sfm)
        result["nerf"] = from_union([lambda x: to_class(Nerf, x), from_none], self.nerf)

        #ingnore null
        result = {k:v for k,v in result.items() if v}
        return result


def scene_from_dict(s: Any) -> Scene:
    return Scene.from_dict(s)


def scene_to_dict(x: Scene) -> Any:
    return to_class(Scene, x)