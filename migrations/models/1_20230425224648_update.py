from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "moderation" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "member" INT NOT NULL,
    "type" SMALLINT NOT NULL  /* GRANTED: 1\nPREVENTED: -1 */,
    "metarole_id" INT NOT NULL REFERENCES "metarole" ("id") ON DELETE CASCADE
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "moderation";"""
