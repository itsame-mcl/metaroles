from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.exceptions import NoValuesFetched
from tortoise.models import Model

if TYPE_CHECKING:
    from model import Condition


class Metarole(Model):
    id = fields.IntField(pk=True)
    guild = fields.IntField()
    conditions: fields.ReverseRelation["Condition"]

    async def is_eligible(self, member_roles: list[int]):
        try:
            required = await self.conditions.filter(type=1).values_list("id", flat=True)
            if all([role in member_roles for role in required]):
                return True
            return False
        except NoValuesFetched:
            return False
