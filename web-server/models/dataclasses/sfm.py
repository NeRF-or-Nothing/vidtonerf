import numpy as np
import numpy.typing as npt
from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast
from models.dataclasses.frame import Frame
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
class Sfm:
    intrinsic_matrix: Optional[npt.NDArray] = None
    frames: Optional[List[Frame]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Sfm':
        assert isinstance(obj, dict)
        intrinsic_matrix = np.array(from_union([lambda x: from_list(lambda x: from_list(from_float, x), x), from_none],
                                               obj.get("intrinsic_matrix")))
        frames = from_union([lambda x: from_list(Frame.from_dict, x), from_none], obj.get("frames"))
        return Sfm(intrinsic_matrix, frames)

    def to_dict(self) -> dict:
        result: dict = {}
        result["intrinsic_matrix"] = from_union([lambda x: from_list(lambda x: from_list(from_float, x), x),
                                                 from_none], self.intrinsic_matrix.tolist())
        result["frames"] = from_union([lambda x: from_list(lambda x: to_class(Frame, x), x), from_none], self.frames)

        #ingnore null
        result = {k:v for k,v in result.items() if v}
        return result