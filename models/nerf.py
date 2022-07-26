from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast
from pymongo import MongoClient


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Nerf:
    model_filepath: str
    rendered_video_filepath: str

    @staticmethod
    def from_dict(obj: Any) -> 'Nerf':
        assert isinstance(obj, dict)
        model_filepath = from_str(obj.get("model_filepath"))
        rendered_video_filepath = from_str(obj.get("rendered_video_filepath"))
        return Nerf(model_filepath, rendered_video_filepath)

    def to_dict(self) -> dict:
        result: dict = {}
        result["model_filepath"] = from_str(self.model_filepath)
        result["rendered_video_filepath"] = from_str(
            self.rendered_video_filepath)
        return result


def nerf_from_dict(s: Any) -> Nerf:
    return Nerf.from_dict(s)


def nerf_to_dict(x: Nerf) -> Any:
    return to_class(Nerf, x)


class NerfManager:
    def __init__(self, db_instance: MongoClient) -> None:
        self.db = db_instance.get_database("nerfdb")
        self.collection = self.db.get_collection("scenes")

    def get_nerf(self, _id: str) -> Nerf:
        return nerf_from_dict(self.collection.find_one({"_id": _id})['nerf'])

    def set_nerf(self, _id: str, nerf: Nerf) -> None:
        self.collection.update_one(
            {"_id": _id}, {"$set": {"nerf": nerf_to_dict(nerf)}})

    def set_nerf_model_filepath(self, _id: str, filepath: str) -> None:
        self.collection.update_one(
            {"_id": _id}, {"$set": {"nerf.model_filepath": filepath}})

    def set_nerf_rendered_video_filepath(self, _id: str, filepath: str) -> None:
        self.collection.update_one(
            {"_id": _id}, {"$set": {"nerf.rendered_video_filepath": filepath}})
