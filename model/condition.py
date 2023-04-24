from tortoise import fields
from tortoise.models import Model

from model import ConditionType, Metarole


class Condition(Model):
    id = fields.IntField(pk=True)
    guild = fields.IntField()
    metarole: fields.ForeignKeyRelation[Metarole] = fields.relational.ForeignKeyField(
        "model.Metarole", to_field="id", on_delete="CASCADE"
    )
    type = fields.IntEnumField(ConditionType)
