from fastapi import APIRouter
from api.database import conn

router = APIRouter()


@router.get("/")
def home():
    return {"message": "Medical Telegram Warehouse API"}


@router.get("/top-products")
def top_products():

    cur = conn.cursor()

    cur.execute("""
        SELECT message_text, views
        FROM raw.telegram_messages
        ORDER BY views DESC NULLS LAST
        LIMIT 10
    """)

    rows = cur.fetchall()

    cur.close()

    return rows


@router.get("/channel-activity")
def channel_activity():

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

    return rows


@router.get("/search")
def search_messages(keyword: str):

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

    return rows


@router.get("/image-stats")
def image_stats():

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

    return rows