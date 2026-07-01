from pydantic import BaseModel
from typing import Optional


# -------------------------
# TOP PRODUCTS
# -------------------------
class TopProductOut(BaseModel):
    message_text: Optional[str]
    views: Optional[int]


# -------------------------
# CHANNEL ACTIVITY (MISSING FIX)
# -------------------------
class ChannelActivityOut(BaseModel):
    channel_name: str
    total_messages: int


# -------------------------
# SEARCH RESULT
# -------------------------
class MessageOut(BaseModel):
    message_id: int
    channel_name: str
    message_text: Optional[str]


# -------------------------
# IMAGE DETECTIONS (YOLO)
# -------------------------
class ImageDetectionResponse(BaseModel):
    message_id: Optional[int]
    channel_name: str
    image_path: str
    detected_object: str
    confidence: float
    image_category: Optional[str]


# -------------------------
# IMAGE STATS (AGGREGATED)
# -------------------------
class ImageStatsOut(BaseModel):
    detected_object: str
    count: int