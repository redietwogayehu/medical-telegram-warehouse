import os
import json
import logging
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from telethon import TelegramClient

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
PHONE = os.getenv("PHONE_NUMBER")

if not API_ID or not API_HASH:
    raise ValueError("Missing TELEGRAM_API_ID or TELEGRAM_API_HASH in .env")

# ----------------------------
# Logging setup
# ----------------------------
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------------------
# Output directories
# ----------------------------
RAW_DIR = "data/raw/telegram_messages"
IMAGE_DIR = "data/raw/images"

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# ----------------------------
# Channels
# ----------------------------
CHANNELS = [
    "CheMed123",
    "LobeliaCosmetics",
    "tikvahpharma"
]

# ----------------------------
# FIXED SESSION PATH (CRITICAL)
# ----------------------------
SESSION_PATH = Path("data/session/telegram_session")
SESSION_PATH.parent.mkdir(parents=True, exist_ok=True)

client = TelegramClient(str(SESSION_PATH), API_ID, API_HASH)

# ----------------------------
# Scrape channel
# ----------------------------
async def scrape_channel(channel_name):
    logging.info(f"Scraping channel: {channel_name}")
    print(f"\n[START] Scraping {channel_name}", flush=True)

    messages_data = []

    try:
        entity = await client.get_entity(channel_name)
        print(f"[OK] Resolved entity: {channel_name}", flush=True)

        count = 0

        async for message in client.iter_messages(entity, limit=200):
            count += 1

            msg = {
                "message_id": message.id,
                "channel_name": channel_name,
                "message_date": str(message.date),
                "message_text": message.message,
                "has_media": bool(message.media),
                "image_path": None,
                "views": message.views,
                "forwards": message.forwards
            }

            if message.media:
                image_path = f"{IMAGE_DIR}/{channel_name}_{message.id}.jpg"
                try:
                    await message.download_media(file=image_path)
                    msg["image_path"] = image_path
                except Exception as e:
                    logging.error(f"Image download failed: {e}")

            messages_data.append(msg)

        print(f"[INFO] Total messages scanned: {count}", flush=True)
        print(f"[INFO] Total messages saved: {len(messages_data)}", flush=True)

    except Exception as e:
        print(f"[ERROR] Failed scraping {channel_name}: {e}", flush=True)
        logging.error(f"{channel_name}: {e}")
        return

    # Save output
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_dir = f"{RAW_DIR}/{date_str}"
    os.makedirs(output_dir, exist_ok=True)

    file_path = f"{output_dir}/{channel_name}.json"

    with open(file_path, "w") as f:
        json.dump(messages_data, f, indent=2)

    print(f"[SAVED] {len(messages_data)} messages → {file_path}", flush=True)


# ----------------------------
# MAIN (SAFE FOR DAGSTER)
# ----------------------------
async def main():
    await client.connect()

    if not await client.is_user_authorized():
        raise Exception(
            "Telegram not authorized. Run: python src/auth_telegram.py"
        )

    print("[INFO] Telegram client started", flush=True)

    for channel in CHANNELS:
        await scrape_channel(channel)

    await client.disconnect()
    print("[INFO] Client disconnected", flush=True)


# ----------------------------
# ENTRY POINT
# ----------------------------
if __name__ == "__main__":
    asyncio.run(main())