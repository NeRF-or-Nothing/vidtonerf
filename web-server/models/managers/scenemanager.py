from pymongo import MongoClient
from typing import Any, List, TypeVar, Callable, Type, cast
from ..dataclasses.scene import Scene, scene_from_dict
from ..dataclasses.video import Video
from ..dataclasses.sfm import Sfm
from ..dataclasses.nerf import Nerf

# dataclasses generated with Quicktype https://github.com/quicktype/quicktype
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = scene_from_dict(json.loads(json_string))

from dataclasses import dataclass



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


class SceneManager:
    def __init__(self, mongoip) -> None:
        client = MongoClient(host=mongoip, port=27017, username="admin", password="password123")
        self.db = client["nerfdb"]
        self.collection = self.db["scenes"]
        self.upsert = True

    # TODO: define set update get and delete for each object
    # adds scene to the collection replacing any existing scene with the same id
    def set_scene(self, _id: str, scene: Scene):
        key = {"_id": _id}
        value = {"$set": scene.to_dict()}
        self.collection.update_one(key, value, upsert=self.upsert)

    def set_video(self, _id: str, vid: Video):
        key = {"_id": _id}
        fields = {"video." + k: v for k, v in vid.to_dict().items()}
        value = {"$set": fields}
        self.collection.update_one(key, value, upsert=self.upsert)

    def set_sfm(self, _id: str, sfn: Sfm):
        key = {"_id": _id}
        fields = {"sfm." + k: v for k, v in sfn.to_dict().items()}
        value = {"$set": fields}
        self.collection.update_one(key, value, upsert=self.upsert)

    def set_nerf(self, _id: str, nerf: Nerf):
        key = {"_id": _id}
        fields = {"nerf." + k: v for k, v in nerf.to_dict().items()}
        value = {"$set": fields}
        self.collection.update_one(key, value, upsert=self.upsert)

    def get_scene(self, _id: str) -> Scene:
        key = {"_id": _id}
        doc = self.collection.find_one(key)
        if doc:
            return scene_from_dict(doc)
        else:
            return None

    def get_video(self, _id: str) -> Video:
        key = {"_id": _id}
        doc = self.collection.find_one(key)
        if doc and "video" in doc:
            return Video.from_dict(doc["video"])
        else:
            return None

    def get_sfm(self, _id: str) -> Sfm:
        key = {"_id": _id}
        doc = self.collection.find_one(key)
        if doc and "sfm" in doc:
            return Sfm.from_dict(doc["sfm"])
        else:
            return None

    def get_nerf(self, _id: str) -> Nerf:
        key = {"_id": _id}
        doc = self.collection.find_one(key)
        if doc and "nerf" in doc:
            return Nerf.from_dict(doc["nerf"])
        else:
            return None