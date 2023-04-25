from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "metarole" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "guild" INT NOT NULL,
    "enabled" INT NOT NULL
);
CREATE TABLE IF NOT EXISTS "condition" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "type" SMALLINT NOT NULL  /* REQUIRED: 1\nFORBIDDEN: -1 */,
    "metarole_id" INT NOT NULL REFERENCES "metarole" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
