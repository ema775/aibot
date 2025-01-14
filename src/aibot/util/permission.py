import os
from typing import Callable, TypeVar

from discord import Interaction, app_commands
from dotenv import load_dotenv

from aibot.sqlite.user_dao import UserDAO

T = TypeVar("T")
userdao = UserDAO()

load_dotenv()
ADMIN_USER_IDS: tuple[int, ...] = tuple(
    map(int, os.getenv("ADMIN_USER_IDS", "").split(",")),
)
ALLOWED_SERVER_IDS: tuple[int, ...] = tuple(
    map(int, os.getenv("ALLOWED_SERVER_IDS", "").split(",")),
)


def is_authorized_server() -> Callable[[T], T]:
    """Check if the server has been authorized by an administrator.

    Returns
    -------
    Callable[[T], T]
        A decorator checks whether the server is listed in the
        environment variable `ALLOWED_SERVER_IDS`.

    """

    def predicate(interaction: Interaction) -> bool:
        return interaction.guild_id in ALLOWED_SERVER_IDS

    return app_commands.check(predicate)


def is_admin_user() -> Callable[[T], T]:
    """Check if the user has administrative permission.

    Returns
    -------
    Callable[[T], T]
        A decorator checks whether the user executing the command is
        listed in the environment variable `ADMIN_USER_IDS`.

    """

    def predicate(interaction: Interaction) -> bool:
        return interaction.user.id in ADMIN_USER_IDS

    return app_commands.check(predicate)


def is_advanced_user() -> Callable[[T], T]:
    """Check if the user has advanced access permission.

    Returns
    -------
    Callable[[T], T]
        A decorator checks whether the user executing the command is
        listed in the advanced user list.

    """

    async def predicate(interaction: Interaction) -> bool:
        advanced_user_ids = await userdao.get_advanced_user_ids()
        return interaction.user.id in advanced_user_ids

    return app_commands.check(predicate)


def is_not_blocked_user() -> Callable[[T], T]:
    """Check if the user is not blocked.

    Returns
    -------
    Callable[[T], T]
        A decorator checks whether the user executing the command is
        not listed in the blocked user list.

    """

    async def predicate(interaction: Interaction) -> bool:
        blocked_user_ids = await userdao.get_blocked_user_ids()
        return interaction.user.id not in blocked_user_ids

    return app_commands.check(predicate)
