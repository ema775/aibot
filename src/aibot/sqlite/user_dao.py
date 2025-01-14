import datetime

import aiosqlite

from aibot.model.time_zone import TIMEZONE
from aibot.model.user_dto import UserDTO
from aibot.sqlite.sqlite_dao_base import SQLiteDAOBase


class UserDAO(SQLiteDAOBase):
    _table_name = "AccessList"

    async def create_table(self) -> None:
        conn = await aiosqlite.connect(super().DB_NAME)
        try:
            await conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self._table_name}
                (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    access_type TEXT NOT NULL,
                    date DATE NOT NULL,
                    rm_date DATE DEFAULT NULL
                );
                """,
            )
            await conn.commit()
        finally:
            await conn.close()

    async def insert_advanced_user(self, user: UserDTO) -> None:
        conn = await aiosqlite.connect(super().DB_NAME)
        date = datetime.datetime.now(TIMEZONE).date()
        try:
            await conn.execute(
                """
                INSERT INTO AccessList (user_id, access_type, date)
                VALUES (?, 'advanced', ?);
                """,
                (user.user_id, date),
            )
            await conn.commit()
        finally:
            await conn.close()

    async def insert_blocked_user(self, user: UserDTO) -> None:
        conn = await aiosqlite.connect(self.DB_NAME)
        date = datetime.datetime.now(TIMEZONE).date()
        try:
            await conn.execute(
                """
                INSERT INTO AccessList (user_id, access_type, date)
                VALUES (?, 'blocked', ?);
                """,
                (user.user_id, date),
            )
            await conn.commit()
        finally:
            await conn.close()

    async def remove_advanced_user(self, user: UserDTO) -> None:
        conn = await aiosqlite.connect(self.DB_NAME)
        date = datetime.datetime.now(TIMEZONE).date()
        try:
            await conn.execute(
                """
                UPDATE AccessList
                SET rm_date=?
                WHERE user_id=? AND access_type='advanced' AND rm_date IS NULL;
                """,
                (date, user.user_id),
            )
            await conn.commit()
        finally:
            await conn.close()

    async def remove_blocked_user(self, user: UserDTO) -> None:
        conn = await aiosqlite.connect(self.DB_NAME)
        date = datetime.datetime.now(TIMEZONE).date()
        try:
            await conn.execute(
                """
                UPDATE AccessList
                SET rm_date=?
                WHERE user_id=? AND access_type='blocked' AND rm_date IS NULL;
                """,
                (date, user.user_id),
            )
            await conn.commit()
        finally:
            await conn.close()

    async def get_advanced_user_ids(self) -> list[int]:
        conn = await aiosqlite.connect(super().DB_NAME)
        try:
            cursor = await conn.execute(
                """
                SELECT user_id FROM AccessList
                WHERE access_type='advanced' AND rm_date IS NULL;
                """,
            )
            rows = await cursor.fetchall()
            return [row[0] for row in rows]
        finally:
            await conn.close()

    async def get_blocked_user_ids(self) -> list[int]:
        conn = await aiosqlite.connect(super().DB_NAME)
        try:
            cursor = await conn.execute(
                """
                SELECT user_id FROM AccessList
                WHERE access_type='blocked' AND rm_date IS NULL;
                """,
            )
            rows = await cursor.fetchall()
            return [row[0] for row in rows]
        finally:
            await conn.close()
