from fastapi import APIRouter, HTTPException
from api.database import get_connection
from api.schemas import (
    TopProductOut,
    ChannelActivityOut,
    MessageOut,
    ImageStatsOut
)

router = APIRouter()


# -------------------------
# HOME
# -------------------------
@router.get("/")
def home():
    return {"message": "Medical Telegram Warehouse API"}


# -------------------------
# TOP PRODUCTS
# -------------------------
@router.get("/top-products", response_model=list[TopProductOut])
def top_products():

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT message_text, views
            FROM raw.telegram_messages
            ORDER BY views DESC NULLS LAST
            LIMIT 10
        """)

        rows = cur.fetchall()

        cur.close()
        conn.close()

        if not rows:
            raise HTTPException(status_code=404, detail="No data found")

        return [
            {"message_text": r[0], "views": r[1]}
            for r in rows
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# CHANNEL ACTIVITY
# -------------------------
@router.get("/channel-activity", response_model=list[ChannelActivityOut])
def channel_activity():

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                channel_name,
                COUNT(*) AS total_messages
            FROM raw.telegram_messages
            GROUP BY channel_name
            ORDER BY total_messages DESC
        """)

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [
            {"channel_name": r[0], "total_messages": r[1]}
            for r in rows
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# SEARCH MESSAGES
# -------------------------
@router.get("/search", response_model=list[MessageOut])
def search_messages(keyword: str):

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                message_id,
                channel_name,
                message_text
            FROM raw.telegram_messages
            WHERE message_text ILIKE %s
            LIMIT 20
        """, (f"%{keyword}%",))

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [
            {
                "message_id": r[0],
                "channel_name": r[1],
                "message_text": r[2]
            }
            for r in rows
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# IMAGE STATS (YOLO)
# -------------------------
@router.get("/image-stats", response_model=list[ImageStatsOut])
def image_stats():

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                detected_object,
                COUNT(*)
            FROM raw.fct_image_detections
            GROUP BY detected_object
            ORDER BY COUNT(*) DESC
        """)

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [
            {"detected_object": r[0], "count": r[1]}
            for r in rows
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))