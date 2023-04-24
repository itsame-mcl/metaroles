from tortoise import fields
from tortoise.models import Model

from model.condition_type import ConditionType


class Condition(Model):
    id = fields.IntField(pk=True)
    guild = fields.IntField()
    metarole = fields.relational.ForeignKeyField(
        "model.Metarole", to_field="id", on_delete="CASCADE"
    )
    type = fields.IntEnumField(ConditionType)
