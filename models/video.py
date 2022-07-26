

from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast
from pymongo import MongoClient


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


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
class Video:
    filepath: str
    width: int
    height: int
    fps: int
    duration: float
    frame_count: int

    @staticmethod
    def from_dict(obj: Any) -> 'Video':
        assert isinstance(obj, dict)
        filepath = from_str(obj.get("filepath"))
        width = from_int(obj.get("width"))
        height = from_int(obj.get("height"))
        fps = from_int(obj.get("fps"))
        duration = from_float(obj.get("duration"))
        frame_count = from_int(obj.get("frame_count"))
        return Video(filepath, width, height, fps, duration, frame_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["filepath"] = from_str(self.filepath)
        result["width"] = from_int(self.width)
        result["height"] = from_int(self.height)
        result["fps"] = from_int(self.fps)
        result["duration"] = to_float(self.duration)
        result["frame_count"] = from_int(self.frame_count)
        return result


def video_from_dict(s: Any) -> Video:
    return Video.from_dict(s)


def video_to_dict(x: Video) -> Any:
    return to_class(Video, x)


class VideoManager:
    def __init__(self, db_instance: MongoClient) -> None:
        self.db = db_instance.get_database("nerfdb")
        self.collection = self.db.get_collection("scenes")

    def get_video(self, _id: str) -> Video:
        return video_from_dict(self.collection.find_one({"_id": _id})['video'])

    def set_video(self, _id: str, video: Video) -> None:
        # video is a field of the video collection document type, so replace the "video" field not the entire document
        self.collection.update_one(
            {"_id": _id}, {"$set": {"video": video_to_dict(video)}})

    def set_video_filepath(self, _id: str, filepath: str) -> None:
        self.collection.update_one(
            {"_id": _id}, {"$set": {"video.filepath": filepath}})

    def set_video_width(self, _id: str, width: int) -> None:
        self.collection.update_one(
            {"_id": _id}, {"$set": {"video.width": width}})

    def set_video_height(self, _id: str, height: int) -> None:
        self.collection.update_one(
            {"_id": _id}, {"$set": {"video.height": height}})

    def set_video_fps(self, _id: str, fps: float) -> None:
        self.collection.update_one(
            {"_id": _id}, {"$set": {"video.fps": fps}})

    def set_video_duration(self, _id: str, duration: float) -> None:
        self.collection.update_one(
            {"_id": _id}, {"$set": {"video.duration": duration}})

    def set_video_frame_count(self, _id: str, frame_count: int) -> None:
        self.collection.update_one(
            {"_id": _id}, {"$set": {"video.frame_count": frame_count}})
