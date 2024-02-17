import numpy as np
import numpy.typing as npt
from pymongo import MongoClient
from dataclasses import dataclass
from typing import List, Any, TypeVar, Callable, Type, cast
from uuid import uuid4
import os
from dotenv import load_dotenv

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

# Load environment variables from .env file at the root of the project
load_dotenv()

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

# QueueList manages list of ids
@dataclass
class QueueList:
    _id: Optional[str] = None
    queue: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'QueueList':
        assert isinstance(obj, dict)
        _id = from_union([from_str, from_none], obj.get("_id"))
        queue = from_union([lambda x:from_list(from_str,x),from_none],obj.get("queue"))
        return QueueList(_id,queue)

    def to_dict(self) -> dict:
        result: dict = {}
        if self._id is not None:
            result["_id"] = from_union([from_str, from_none], self._id)
        if self.queue is not None:
            result["queue"] = from_union([lambda x: from_list(from_str, x), from_none], self.queue)
        return result

# QueueListManager keeps track of lists (queues) in parallel with RabbitMQ to report queue status
# VALID QUEUE IDS: sfm_list nerf_list queue_lit (queue_list is the overarching process)
class QueueListManager:
    def __init__(self,mongoip) -> None:
        client = MongoClient(host=mongoip,port=27017,username="admin",password="password123")
        self.db = client["nerfdb"]
        self.collection = self.db["queues"]
        self.upsert=True
        # Valid queue ids:
        self.queue_names = ["sfm_list","nerf_list","queue_list"]

    # Set a queue list
    def __set_queue(self, _id: str, queue_list: QueueList):
        if _id not in self.queue_names:
            raise Exception("Not a valid queue ID. Valid queue IDs: {}".format(self.queue_names))
        key = {"_id":_id}
        value = {"$set": queue_list.to_dict()}
        self.collection.update_one(key, value, upsert=self.upsert)

    # Append a uuid to the queue list
    def append_queue(self, queueid: str, uuid: str):
        # Check for valid queue id
        if queueid not in self.queue_names:
            raise Exception("Not a valid queue ID. Valid queue IDs: {}".format(self.queue_names))
        # Create queue or add to existing queue
        doc = self.collection.find_one(queueid)
        if not doc:
            self.__set_queue(queueid,QueueList(queueid,[uuid]))
        else:
            queue_list = QueueList.from_dict(doc)
            # Make sure ID is not in list already
            x = [x for x in queue_list.queue if x == uuid]
            if len(x) > 0:
                raise Exception("ID is already in the queue!")
            # Append queue
            queue_list.queue.append(uuid)
            self.__set_queue(queueid,queue_list)

    # Get a position in the queue list
    def get_queue_position(self, queueid: str, uuid: str) -> 'tuple[int,int]':
        # Check for valid queue id
        if queueid not in self.queue_names:
            raise Exception("Not a valid queue ID. Valid queue IDs: {}".format(self.queue_names))
        doc = self.collection.find_one(queueid)
        queue_list = QueueList.from_dict(doc)
        # Obtain indices of all occurences of the uuid
        x = [x for x in range(0,len(queue_list.queue)) if queue_list.queue[x] == uuid]
        if len(x) > 1:
            raise Exception("Same ID found multiple times in queue!")
        elif len(x) == 0:
            raise Exception("ID not found in queue!")
        else:
            return (x[0], len(queue_list.queue))
    
    # Returns the size of a queue
    def get_queue_size(self, queueid: str) -> int:
        if queueid not in self.queue_names:
            raise Exception("Not a valid queue ID. Valid queue IDs: {}".format(self.queue_names))
        doc = self.collection.find_one(queueid)
        queue_list = QueueList.from_dict(doc)
        return len(queue_list.queue)
    
    # Pops either a given uuid or the first uuid of a list
    def pop_queue(self, queueid: str, uuid: str=None):
        # Check if valid queue id
        if queueid not in self.queue_names:
            raise Exception("Not a valid queue ID. Valid queue IDs: {}".format(self.queue_names))
        doc = self.collection.find_one(queueid)
        queue_list = QueueList.from_dict(doc)
        # Check that the uuid exists or no uuid was provided
        if len(queue_list.queue) == 0 or (uuid and uuid not in queue_list.queue):
            raise Exception("Queue empty or ID not found!")
        if uuid:
            queue_list.queue.remove(uuid)
        else:
            queue_list.queue.pop(0)
        self.__set_queue(queueid, queue_list)


class SceneManager:
    def __init__(self) -> None:
        client = MongoClient(host=os.getenv("MONGO_IP"),port=27017,username=os.getenv("MONGO_INITDB_ROOT_USERNAME"),\
                             password=os.getenv("MONGO_INITDB_ROOT_PASSWORD"))
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
            return Nerf.from_dict(doc["nerf"])
        else:
            return None
        

class UserManager:
    def __init__(self) -> None:
        client = MongoClient(host=os.getenv("MONGO_IP"),port=27017,username=os.getenv("MONGO_INITDB_ROOT_USERNAME"),\
                             password=os.getenv("MONGO_INITDB_ROOT_PASSWORD"))
        self.db = client["nerfdb"]
        self.collection = self.db["users"]
        self.upsert=True


    def set_user(self, user:User):  #usernames and ids are forced to be unique, passwords are not
        key={"username":user.username}
        doc = self.collection.find_one(key)
        if doc!=None:
            #Two users assigned with same username
            return 1
        key={"_id":user._id}
        doc = self.collection.find_one(key)
        if doc!=None:
            raise Exception('Two users assigned with same ID!')
        user.password=str(hash(user.password))

        value = {"$set": user.to_dict()}
        self.collection.update_one(key,value,upsert=self.upsert)
        return 0

    def generate_user(self, username:str, password:str):
        _id = str(uuid4())
        user=User(username,password,_id)
        errorcode=self.set_user(user)
        if(errorcode!=0):
            return errorcode
            
        return user
            

    def get_user_by_id(self, _id: str) -> User:
        key = {"_id":_id}
        doc = self.collection.find_one(key)
        if doc:
            return User.from_dict(doc)
        else:
            return None

    def get_user_by_username(self, username: str) -> User:
        key = {"username":username}
        doc = self.collection.find_one(key)
        if doc:
            return User.from_dict(doc)
        else:
            return None
    #TODO: Write an overloaded function for finding users by username
         

