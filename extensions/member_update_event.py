from interactions import Extension, listen
from interactions.api.events import MemberUpdate
from tortoise.exceptions import NoValuesFetched

from core.base import CustomClient
from model import Metarole


class MemberUpdateEvent(Extension):
    bot: CustomClient

    @listen()
    async def on_member_update(self, event: MemberUpdate):
        roles_before = set(event.before.roles) if event.before.roles else set()
        roles_after = set(event.after.roles) if event.after.roles else set()
        role_added = roles_after.difference(roles_before)
        role_deleted = roles_before.difference(roles_after)
        role_updated = list(role_added.union(role_deleted))[0]
        self.bot.logger.debug(f"Role updated : {role_updated}")
        metaroles = await Metarole.filter(conditions__id=role_updated)
        for metarole in metaroles:
            try:
                is_eligible = True
                for condition in await metarole.conditions.all():
                    self.bot.logger.debug(f"Challenged condition : {condition.id}")
                    is_eligible = is_eligible and event.after.has_role(condition.id)
                    self.bot.logger.debug(f"Is still eligible ? {is_eligible}")
            except NoValuesFetched:
                is_eligible = False
            if is_eligible and not event.after.has_role(metarole.id):
                self.bot.logger.debug(f"Metarole to add : {metarole.id}")
                await event.after.add_role(metarole.id)
            if not is_eligible and event.after.has_role(metarole.id):
                self.bot.logger.debug(f"Metarole to delete : {metarole.id}")
                await event.after.remove_role(metarole.id)


def setup(bot: CustomClient):
    """Let naff load the extension"""

    MemberUpdateEvent(bot)
