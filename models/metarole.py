from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.exceptions import NoValuesFetched
from tortoise.models import Model

from models import ModerationType

if TYPE_CHECKING:
    from models import Condition, Moderation


class Metarole(Model):
    id = fields.IntField(pk=True)
    guild = fields.IntField()
    enabled = fields.BooleanField()
    conditions: fields.ReverseRelation["Condition"]
    moderations: fields.ReverseRelation["Moderation"]

    async def is_eligible(self, member_id: int, member_roles: list[int]):
        try:
            required = await self.conditions.filter(type=1).values_list("id", flat=True)
            forbidden = await self.conditions.filter(type=-1).values_list(
                "id", flat=True
            )
            moderation_status = (
                await self.moderations.filter(member=member_id)
                .get_or_none()
                .values_list("type", flat=True)
            )
            if (moderation_status and moderation_status == ModerationType.GRANTED) or (
                all([role in member_roles for role in required])
                and not any([role in member_roles for role in forbidden])
                and not (
                    moderation_status and moderation_status == ModerationType.PREVENTED
                )
            ):
                return True
            return False
        except NoValuesFetched:
            return False
