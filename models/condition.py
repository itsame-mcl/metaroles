from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.models import Model

from models import ConditionType

if TYPE_CHECKING:
    from models import Metarole


class Condition(Model):
    id = fields.IntField(pk=True)
    guild = fields.IntField()
    metarole: fields.ForeignKeyRelation["Metarole"] = fields.relational.ForeignKeyField(
        "models.Metarole", to_field="id", on_delete="CASCADE"
    )
    type = fields.IntEnumField(ConditionType)
