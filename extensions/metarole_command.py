from interactions import (
    Extension,
    OptionType,
    Role,
    SlashContext,
    slash_command,
    slash_option,
)

from core.base import CustomClient
from model import Condition, ConditionType, Metarole


class MetaRoleCommand(Extension):
    bot: CustomClient

    @slash_command(
        name="metarole",
        description="Meta-roles management",
        sub_cmd_name="add",
        sub_cmd_description="Add a meta-role",
    )
    @slash_option(
        name="granted_role",
        description="Name of the granted role",
        required=True,
        opt_type=OptionType.ROLE,
    )
    @slash_option(
        name="first_required",
        description="Name of the first required role",
        required=True,
        opt_type=OptionType.ROLE,
    )
    @slash_option(
        name="second_required",
        description="Name of the second required role",
        required=True,
        opt_type=OptionType.ROLE,
    )
    async def metarole_add(
        self,
        ctx: SlashContext,
        granted_role: Role,
        first_required: Role,
        second_required: Role,
    ):
        guild_id = int(ctx.guild.id)
        await Metarole.create(id=int(granted_role.id), guild=guild_id)
        await Condition.create(
            id=int(first_required.id),
            guild=guild_id,
            metarole_id=int(granted_role.id),
            type=ConditionType.REQUIRED,
        )
        await Condition.create(
            id=int(second_required.id),
            guild=guild_id,
            metarole_id=int(granted_role.id),
            type=ConditionType.REQUIRED,
        )
        await ctx.send("Metarole created")


def setup(bot: CustomClient):
    """Let interactions load the extension"""

    MetaRoleCommand(bot)
