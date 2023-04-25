from interactions import (
    Extension,
    OptionType,
    Role,
    SlashContext,
    slash_command,
    slash_option,
)
from interactions.client.utils import get_all

from core.base import CustomClient
from models import Condition, ConditionType, Metarole


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
        await Metarole.create(id=int(granted_role.id), enabled=False, guild=guild_id)
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

    @slash_command(
        name="metarole",
        description="Meta-roles management",
        sub_cmd_name="enable",
        sub_cmd_description="Add a meta-role",
    )
    @slash_option(
        name="role",
        description="Name of the meta role to enable",
        required=True,
        opt_type=OptionType.ROLE,
    )
    async def metarole_enable(self, ctx: SlashContext, role: Role):
        metarole = await Metarole.filter(
            id=int(role.id), guild=int(ctx.guild.id)
        ).get_or_none()
        if metarole:
            await metarole.update_from_dict({"enabled": True}).save()
            await ctx.send("Metarole enabled")
        else:
            await ctx.send("This is not a metarole")

    @slash_command(
        name="metarole",
        description="Meta-roles management",
        sub_cmd_name="disable",
        sub_cmd_description="Add a meta-role",
    )
    @slash_option(
        name="role",
        description="Name of the meta role to enable",
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
        for member in members:
            member_roles = [int(role.id) for role in member.roles]
            for metarole in metaroles:
                is_eligible = await metarole.is_eligible(member_roles)
                if is_eligible and int(metarole.id) not in member_roles:
                    await member.add_role(metarole.id)
                if not is_eligible and int(metarole.id) in member_roles:
                    await member.remove_role(metarole.id)
        await ctx.send("Check OK")


def setup(bot: CustomClient):
    """Let interactions load the extension"""

    MetaRoleCommand(bot)
