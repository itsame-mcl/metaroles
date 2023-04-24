from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.models import Model

if TYPE_CHECKING:
    from model import Condition


class Metarole(Model):
    id = fields.IntField(pk=True)
    guild = fields.IntField()
    conditions: fields.ReverseRelation["Condition"]
