import os

from dotenv import load_dotenv
from interactions import Intents
from interactions.ext.debug_extension import DebugExtension
from tortoise import run_async

from core.base import CustomClient
from core.extensions_loader import load_extensions
from core.init_logging import init_logging
from core.init_tortoise import init_tortoise

if __name__ == "__main__":
    # load the environmental vars from the .env file
    load_dotenv()

    # initialise logging
    init_logging()

    # initialise tortoise
    run_async(init_tortoise())

    # create our bot instance
    bot = CustomClient(
        intents=Intents.new(
            default=True, guild_members=True
        ),  # intents are what events we want to receive from discord, `DEFAULT` is usually fine
        auto_defer=True,  # automatically deferring interactions
        activity="Meta-roles manager",  # the status message of the bot
        fetch_members=True,
    )

    # enable Sentry.io observability if sentry DSN is provided
    if os.getenv("SENTRY_DSN"):
        bot.load_extension("interactions.ext.sentry", token=os.getenv("SENTRY_DSN"))

    # load the debug extension if that is wanted
    if os.getenv("LOAD_DEBUG_COMMANDS") == "true":
        DebugExtension(bot=bot)

    # load all extensions in the ./extensions folder
    load_extensions(bot=bot)

    # start the bot
    bot.start(os.getenv("DISCORD_TOKEN"))
