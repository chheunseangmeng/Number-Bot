import os
import aiomysql
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "db": os.getenv("DB_NAME", "number_bot"),
    "autocommit": True,
}

pool = None


async def init_db():
    global pool
    pool = await aiomysql.create_pool(**DB_CONFIG)
    print("[DB] Connected successfully.", flush=True)


async def close_db():
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()
        print("[DB] Connection closed.", flush=True)


# ─── User Queries ─────────────────────────────────────────────

async def get_or_create_user(
    telegram_id: int,
    full_name: str,
    username: str,
    start_param: str = None,
) -> int:
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT id FROM users WHERE telegram_id = %s",
                (telegram_id,),
            )
            row = await cur.fetchone()
            if row:
                return row[0]

            await cur.execute(
                """
                INSERT INTO users (telegram_id, full_name, username, start_param)
                VALUES (%s, %s, %s, %s)
                """,
                (telegram_id, full_name, username, start_param),
            )
            return cur.lastrowid


async def update_user_phone(telegram_id: int, phone_number: str) -> None:
    """Called when user shares their contact/phone number."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE users SET phone_number = %s WHERE telegram_id = %s",
                (phone_number, telegram_id),
            )


async def get_user_by_telegram_id(telegram_id: int) -> dict | None:
    """Fetch full user row including phone_number."""
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "SELECT * FROM users WHERE telegram_id = %s",
                (telegram_id,),
            )
            return await cur.fetchone()


# ─── Game Queries ─────────────────────────────────────────────

async def save_games(user_id: int, games: list[list[int]]) -> None:
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            for game in games:
                await cur.execute(
                    """
                    INSERT INTO games (user_id, number_1, number_2)
                    VALUES (%s, %s, %s)
                    """,
                    (user_id, game[0], game[1]),
                )


# ─── Receipt Queries ──────────────────────────────────────────

async def save_receipt(
    transaction_id: str,
    user_id: int,
    bank_name: str,
    amount: float,
) -> int:
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO receipts (transaction_id, user_id, bank_name, amount)
                VALUES (%s, %s, %s, %s)
                """,
                (transaction_id, user_id, bank_name, amount),
            )
            return cur.lastrowid