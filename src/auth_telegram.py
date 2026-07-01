from telethon import TelegramClient
from pathlib import Path
import asyncio

API_ID = 31784753
API_HASH = "0ed74bb8159bba6aaadccd86760f642b"

# -------------------------
# FIXED SESSION LOCATION
# -------------------------
SESSION_DIR = Path("data/session")
SESSION_DIR.mkdir(parents=True, exist_ok=True)

SESSION_PATH = str(SESSION_DIR / "telegram_session")

client = TelegramClient(SESSION_PATH, API_ID, API_HASH)


async def main():
    await client.start()
    print("AUTH SUCCESS - session saved at:", SESSION_PATH)


if __name__ == "__main__":
    asyncio.run(main())