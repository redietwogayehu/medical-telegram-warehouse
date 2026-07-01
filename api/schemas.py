from pydantic import BaseModel
from typing import List, Optional


class ImageDetectionResponse(BaseModel):
    message_id: Optional[int]
    channel_name: str
    image_path: str
    detected_object: str
    confidence: float
    image_category: Optional[str]


class ChannelStatsResponse(BaseModel):
    channel_name: str
    total_messages: int
    total_images: int