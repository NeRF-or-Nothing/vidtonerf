import numpy as np
import numpy.typing as npt
from pymongo import MongoClient
from dataclasses import dataclass
from typing import List, Any, TypeVar, Callable, Type, cast

# dataclasses generated with Quicktype https://github.com/quicktype/quicktype
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = scene_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast


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
class Nerf:
    model_file_path: Optional[str] = None
    rendered_video_path: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Nerf':
        assert isinstance(obj, dict)
        model_file_path = from_union([from_str, from_none], obj.get("model_file_path"))
        rendered_video_path = from_union([from_str, from_none], obj.get("rendered_video_path"))
        return Nerf(model_file_path, rendered_video_path)

    def to_dict(self) -> dict:
        result: dict = {}
        result["model_file_path"] = from_union([from_str, from_none], self.model_file_path)
        result["rendered_video_path"] = from_union([from_str, from_none], self.rendered_video_path)

        #ingnore null
        result = {k:v for k,v in result.items() if v}
        return result


@dataclass
class Frame:
    file_path: Optional[str] = None
    extrinsic_matrix: Optional[npt.NDArray] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Frame':
        assert isinstance(obj, dict)
        file_path = from_union([from_str, from_none], obj.get("file_path"))
        extrinsic_matrix = np.array(from_union([lambda x: from_list(lambda x: from_list(from_float, x), x), from_none], obj.get("extrinsic_matrix")))
        return Frame(file_path, extrinsic_matrix)

    def to_dict(self) -> dict:
        result: dict = {}
        result["file_path"] = from_union([from_str, from_none], self.file_path)
        result["extrinsic_matrix"] = from_union([lambda x: from_list(lambda x: from_list(from_float, x), x), from_none], self.extrinsic_matrix.tolist())

        #ingnore null
        result = {k:v for k,v in result.items() if v}
        return result


@dataclass
class Sfm:
    intrinsic_matrix: Optional[npt.NDArray] = None
    frames: Optional[List[Frame]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Sfm':
        assert isinstance(obj, dict)
        intrinsic_matrix = np.array(from_union([lambda x: from_list(lambda x: from_list(from_float, x), x), from_none], obj.get("intrinsic_matrix")))
        frames = from_union([lambda x: from_list(Frame.from_dict, x), from_none], obj.get("frames"))
        return Sfm(intrinsic_matrix, frames)

    def to_dict(self) -> dict:
        result: dict = {}
        result["intrinsic_matrix"] = from_union([lambda x: from_list(lambda x: from_list(from_float, x), x), from_none], self.intrinsic_matrix.tolist())
        result["frames"] = from_union([lambda x: from_list(lambda x: to_class(Frame, x), x), from_none], self.frames)

        #ingnore null
        result = {k:v for k,v in result.items() if v}
        return result


@dataclass
class Video:
    file_path: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[int] = None
    duration: Optional[int] = None
    frame_count: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Video':
        assert isinstance(obj, dict)
        file_path = from_union([from_str, from_none], obj.get("file_path"))
        width = from_union([from_int, from_none], obj.get("width"))
        height = from_union([from_int, from_none], obj.get("height"))
        fps = from_union([from_float, from_none], obj.get("fps"))
        duration = from_union([from_float, from_none], obj.get("duration"))
        frame_count = from_union([from_int, from_none], obj.get("frame_count"))
        return Video(file_path, width, height, fps, duration, frame_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["file_path"] = from_union([from_str, from_none], self.file_path)
        result["width"] = from_union([from_int, from_none], self.width)
        result["height"] = from_union([from_int, from_none], self.height)
        result["fps"] = from_union([from_float, from_none], self.fps)
        result["duration"] = from_union([from_float, from_none], self.duration)
        result["frame_count"] = from_union([from_int, from_none], self.frame_count)

        #ingnore null
        result = {k:v for k,v in result.items() if v}
        return result


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


class SceneManager:
    def __init__(self) -> None:
        client = MongoClient(host="mongodb",port=27017,username="admin",password="password123")
        self.db = client["nerfdb"]
        self.collection = self.db["scenes"]
        self.upsert=True
    
    #TODO: define set update get and delete for each object 
    # adds scene to the collection replacing any existing scene with the same id
    def set_scene(self, _id: str, scene: Scene):
        key = {"_id": _id}
        value = {"$set": scene.to_dict()}
        self.collection.update_one(key, value, upsert=self.upsert)

    def set_video(self, _id: str, vid: Video):
        key = {"_id":_id}
        fields = {"video."+k:v for k,v in vid.to_dict().items()}
        value = {"$set": fields}
        self.collection.update_one(key, value, upsert=self.upsert)

    def set_sfm(self, _id: str, sfn: Sfm):
        key = {"_id":_id}
        fields = {"sfm."+k:v for k,v in sfn.to_dict().items()}
        value = {"$set": fields}
        self.collection.update_one(key, value, upsert=self.upsert)

    def set_nerf(self, _id: str, nerf: Nerf):
        key = {"_id":_id}
        fields = {"nerf."+k:v for k,v in nerf.to_dict().items()}
        value = {"$set": fields}
        self.collection.update_one(key, value, upsert=self.upsert)

    def get_scene(self, _id: str) -> Scene:
        key = {"_id":_id}
        doc = self.collection.find_one(key)
        if doc:
            return scene_from_dict(doc)
        else:
            return None

    def get_video(self, _id: str) -> Video:
        key = {"_id":_id}
        doc = self.collection.find_one(key)
        if doc and "video" in doc:
            return Video.from_dict(doc["video"])
        else:
            return None

    def get_sfm(self, _id: str) -> Sfm:
        key = {"_id":_id}
        doc = self.collection.find_one(key)
        if doc and "sfm" in doc:
            return Sfm.from_dict(doc["sfm"])
        else:
            return None
    
    def get_nerf(self, _id: str) -> Nerf:
        key = {"_id":_id}
        doc = self.collection.find_one(key)
        if doc and "nerf" in doc:
            return Sfm.from_dict(doc["nerf"])
        else:
            return None
