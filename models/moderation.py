from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.models import Model

from models import ModerationType

if TYPE_CHECKING:
    from models import Metarole


class Moderation(Model):
    id = fields.IntField(pk=True)
    member = fields.IntField()
    metarole: fields.ForeignKeyRelation["Metarole"] = fields.relational.ForeignKeyField(
        "models.Metarole", to_field="id", on_delete="CASCADE"
    )
    type = fields.IntEnumField(ModerationType)
