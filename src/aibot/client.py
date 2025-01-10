import discord
from discord import Client, app_commands

from aibot.util.logging_setup import logger

# ------ Intents Settings ------ #
intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class AiBotClient(Client):
    tree: app_commands.CommandTree
    _instance: "AiBotClient"

    async def on_ready(self) -> None:
        """Event handler for when the application is ready to start."""
        logger.info("We have logged in as %s", self.user)
        bot_application_info = await self.application_info()
        application_id = bot_application_info.id
        logger.info("Application ID: %s", application_id)
        await self.tree.sync()

    @classmethod
    def get_instance(cls) -> "AiBotClient":
        """Get the instance of the AiBotClient class.

        Parameters
        ----------
        None

        Returns
        -------
        AiBotClient
            The instance of the AiBotClient class.

        """
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        super().__init__(intents=intents)
        AiBotClient.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await AiBotClient.tree.sync()

    async def cleanup_hook(self) -> None:
        logger.info("Start cleanup...")
