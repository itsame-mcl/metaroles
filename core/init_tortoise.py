from aerich import Command

TORTOISE_ORM = {
    "connections": {"default": "sqlite://data/db.sqlite3"},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        }
    },
}


async def init_tortoise():
    command = Command(tortoise_config=TORTOISE_ORM, app="models")
    await command.init()
    await command.upgrade()
