from base64 import b64decode
from typing import List, Optional
from datetime import datetime

from confluent_kafka import Message
from pydantic import BaseModel as pdbm, Field, field_validator, ValidationInfo


class BaseModel(pdbm):
    def to_bytes(self):
        return self.model_dump_json(exclude_none=True, by_alias=True).encode()

    @classmethod
    def from_kafka(cls, msg: Message):
        return cls.model_validate_json(msg.value())


class Location(BaseModel):
    partition: int
    offset: int
    topic: str


class Dimensions(BaseModel):
    width: int
    height: int


class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class Frame(BaseModel):
    location: Optional[Location] = None
    dimensions: Optional[Dimensions] = None
    regions: Optional[List[BoundingBox]] = None


class Camera(BaseModel):
    name: str
    group: str
    modules: List[str]


class Producer(BaseModel):
    camera: Optional[Camera]
    id: str
    name: str


class Object(BaseModel):
    obj_class: str = Field(alias="class")
    bounding_box: BoundingBox
    confidence: float
    user_data: Optional[dict] = None


class DetectionMessage(BaseModel):
    frame: Optional[Frame]
    type: str
    producer: Producer
    timestamp: datetime = Field(
        default_factory=lambda: datetime.utcnow().astimezone())
    detections: List[Object]


class FrameMessage(BaseModel):
    frame: Frame
    type: str
    producer: Producer
    data: bytes

    @field_validator("data", mode="before")
    @classmethod
    def frame_converter(cls, val: str, _: ValidationInfo) -> bytes:
        return b64decode(val)
