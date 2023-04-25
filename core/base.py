import logging
import os

from interactions import Client, Member, listen, logger_name

from models import Metarole


class CustomClient(Client):
    """Subclass of naff.Client with our own logger and on_startup event"""

    # you can use that logger in all your extensions
    logger = logging.getLogger(logger_name)

    @listen()
    async def on_startup(self):
        """Gets triggered on startup"""

        self.logger.info(f"{os.getenv('PROJECT_NAME')} - Startup Finished!")
        self.logger.info(
            "Note: Discord needs up to an hour to load your global commands / context menus. They may not appear immediately\n"
        )

    async def check_metarole(self, metarole: Metarole, members: list[Member]):
        for member in members:
            member_roles = [int(role.id) for role in member.roles]
            is_eligible = await metarole.is_eligible(int(member.id), member_roles)
            if is_eligible and int(metarole.id) not in member_roles:
                self.logger.debug(f"Metarole to add : {metarole.id}")
                await member.add_role(metarole.id)
            if not is_eligible and int(metarole.id) in member_roles:
                self.logger.debug(f"Metarole to delete : {metarole.id}")
                await member.remove_role(metarole.id)
