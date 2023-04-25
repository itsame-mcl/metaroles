from interactions import Extension, listen
from interactions.api.events import MemberUpdate

from core.base import CustomClient
from models import Metarole


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
        metaroles = await Metarole.filter(
            guild=int(event.guild.id), enabled=True, conditions__id=role_updated
        )
        for metarole in metaroles:
            member_roles = [int(role.id) for role in event.after.roles]
            is_eligible = await metarole.is_eligible(member_roles)
            if is_eligible and not event.after.has_role(metarole.id):
                self.bot.logger.debug(f"Metarole to add : {metarole.id}")
                await event.after.add_role(metarole.id)
            if not is_eligible and event.after.has_role(metarole.id):
                self.bot.logger.debug(f"Metarole to delete : {metarole.id}")
                await event.after.remove_role(metarole.id)


def setup(bot: CustomClient):
    """Let naff load the extension"""

    MemberUpdateEvent(bot)
