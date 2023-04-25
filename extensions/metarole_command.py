from typing import Optional

from interactions import (
    Extension,
    OptionType,
    Role,
    SlashCommandChoice,
    SlashContext,
    slash_command,
    slash_option,
)
from interactions.client.utils import get_all

from core.base import CustomClient
from models import Condition, Metarole


class MetaRoleCommand(Extension):
    bot: CustomClient

    @staticmethod
    async def __get_metarole(guild_id: int, metarole_id: int) -> Optional[Metarole]:
        return await Metarole.filter(
            id=int(metarole_id), guild=int(guild_id)
        ).get_or_none()

    @staticmethod
    async def __get_condition(
        metarole_id: int, condition_id: int
    ) -> Optional[Condition]:
        return await Condition.filter(
            id=condition_id, metarole_id=metarole_id
        ).get_or_none()

    @slash_command(
        name="metarole",
        description="Meta-roles management",
        sub_cmd_name="add",
        sub_cmd_description="Add a meta-role",
    )
    @slash_option(
        name="meta_role",
        description="Name of the meta-role",
        required=True,
        opt_type=OptionType.ROLE,
    )
    async def metarole_add(self, ctx: SlashContext, meta_role: Role):
        await Metarole.create(
            id=int(meta_role.id), enabled=False, guild=int(ctx.guild.id)
        )
        await ctx.send("Metarole created")

    @slash_command(
        name="metarole",
        description="Meta-roles management",
        group_name="condition",
        group_description="Constraints management",
        sub_cmd_name="add",
        sub_cmd_description="Add a condition to a meta-role",
    )
    @slash_option(
        name="meta_role",
        description="Name of the meta-role",
        required=True,
        opt_type=OptionType.ROLE,
    )
    @slash_option(
        name="condition_role",
        description="Name of the constraint role",
        required=True,
        opt_type=OptionType.ROLE,
    )
    @slash_option(
        name="condition_type",
        description="Type of the constraint",
        required=True,
        opt_type=OptionType.INTEGER,
        choices=[
            SlashCommandChoice(name="Required", value=1),
            SlashCommandChoice(name="Forbidden", value=-1),
        ],
    )
    async def condition_add(
        self,
        ctx: SlashContext,
        meta_role: Role,
        condition_role: Role,
        condition_type: int,
    ):
        metarole = await self.__get_metarole(int(ctx.guild.id), int(meta_role.id))
        if metarole:
            await Condition.create(
                id=int(condition_role.id),
                metarole_id=int(meta_role.id),
                type=condition_type,
            )
            await ctx.send("Condition enabled")
        else:
            await ctx.send(f"{meta_role.name} is not a meta-role")

    @slash_command(
        name="metarole",
        description="Meta-roles management",
        group_name="condition",
        group_description="Conditions management",
        sub_cmd_name="delete",
        sub_cmd_description="Delete a condition from a meta-role",
    )
    @slash_option(
        name="meta_role",
        description="Name of the meta-role",
        required=True,
        opt_type=OptionType.ROLE,
    )
    @slash_option(
        name="condition_role",
        description="Name of the condition role",
        required=True,
        opt_type=OptionType.ROLE,
    )
    async def condition_delete(
        self, ctx: SlashContext, meta_role: Role, condition_role: Role
    ):
        metarole = await self.__get_metarole(int(ctx.guild.id), int(meta_role.id))
        condition = await self.__get_condition(
            int(meta_role.id), int(condition_role.id)
        )
        if metarole and condition:
            await condition.delete()
            await ctx.send("Condition deleted")
        else:
            await ctx.send(
                f"{meta_role.name} is not a meta-role or {condition_role.name} is not on this conditions"
            )

    @slash_command(
        name="metarole",
        description="Meta-roles management",
        sub_cmd_name="enable",
        sub_cmd_description="Enable a meta-role",
    )
    @slash_option(
        name="role",
        description="Name of the meta role to enable",
        required=True,
        opt_type=OptionType.ROLE,
    )
    async def metarole_enable(self, ctx: SlashContext, role: Role):
        metarole = await self.__get_metarole(int(ctx.guild.id), int(role.id))
        if metarole:
            await metarole.update_from_dict({"enabled": True}).save()
            await ctx.send("Metarole enabled")
        else:
            await ctx.send("This is not a metarole")

    @slash_command(
        name="metarole",
        description="Meta-roles management",
        sub_cmd_name="disable",
        sub_cmd_description="Disable a meta-role",
    )
    @slash_option(
        name="role",
        description="Name of the meta role to disable",
        required=True,
        opt_type=OptionType.ROLE,
    )
    async def metarole_disable(self, ctx: SlashContext, role: Role):
        metarole = await Metarole.filter(
            id=int(role.id), guild=int(ctx.guild.id)
        ).get_or_none()
        if metarole:
            await metarole.update_from_dict({"enabled": False}).save()
            await ctx.send("Metarole disabled")
        else:
            await ctx.send("This is not a metarole")

    @slash_command(
        name="metarole",
        description="Meta-roles management",
        sub_cmd_name="check",
        sub_cmd_description="Check for all meta-roles",
    )
    async def metarole_check(self, ctx: SlashContext):
        members = get_all(ctx.guild.members)
        metaroles = await Metarole.filter(guild=int(ctx.guild.id))
        for metarole in metaroles:
            await self.bot.check_metarole(metarole, members)
        await ctx.send("Check OK")


def setup(bot: CustomClient):
    """Let interactions load the extension"""

    MetaRoleCommand(bot)
