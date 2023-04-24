from tortoise import fields
from tortoise.models import Model

from model import Condition


class Metarole(Model):
    id = fields.IntField(pk=True)
    guild = fields.IntField()
    conditions: fields.ReverseRelation["Condition"]
