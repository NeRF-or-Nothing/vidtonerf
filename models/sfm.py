import numpy as np
from pymongo import MongoClient

import numpy.typing as npt
from dataclasses import dataclass
from typing import List, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")
def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x

def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]

def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x

def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()

@dataclass
class Frame:
    file_path: str
    extrinsic_matrix: npt.NDArray

    @staticmethod
    def from_dict(obj: Any) -> 'Frame':
        assert isinstance(obj, dict)
        file_path = from_str(obj.get("file_path"))
        extrinsic_matrix = np.array(from_list(lambda x: from_list(from_int, x), obj.get("extrinsic_matrix")))
        return Frame(file_path, extrinsic_matrix)

    def to_dict(self) -> dict:
        result: dict = {}
        result["file_path"] = from_str(self.file_path)
        result["extrinsic_matrix"] = from_list(lambda x: from_list(from_int, x), self.extrinsic_matrix.tolist())
        return result


@dataclass
class Sfm:
    intrinsic_matrix: npt.NDArray
    frames: List[Frame]

    @staticmethod
    def from_dict(obj: Any) -> 'Sfm':
        assert isinstance(obj, dict)
        intrinsic_matrix = np.array(from_list(lambda x: from_list(from_int, x), obj.get("intrinsic_matrix")))
        frames = from_list(Frame.from_dict, obj.get("frames"))
        return Sfm(intrinsic_matrix, frames)

    def to_dict(self) -> dict:
        result: dict = {}
        result["intrinsic_matrix"] = from_list(lambda x: from_list(from_int, x), self.intrinsic_matrix.tolist())
        result["frames"] = from_list(lambda x: to_class(Frame, x), self.frames)
        return result

def sfm_from_dict(s: Any) -> Sfm:
    return Sfm.from_dict(s)

def sfm_to_dict(x: Sfm) -> Any:
    return to_class(Sfm, x)


class SfmManager:
    def __init__(self, db_instance: MongoClient) -> None:
        self.db = db_instance.get_database("nerfdb")
        self.collection = self.db.get_collection("scenes")

    def get_sfm(self, _id: str) -> Sfm:
        return sfm_from_dict(self.collection.find_one({"_id": _id})["sfm"])

    def set_sfm(self,_id: str, sfm: Sfm) -> None:
        self.collection.update_one({"_id":_id}, {"$set": {"sfm": sfm_to_dict(sfm)}})
    
    def delete_sfm(self,_id: str) -> None:
        self.collection.update_one({"_id": _id}, {"$unset": {"sfm": ""} })

