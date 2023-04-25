from typing import Optional

from interactions import (
    Extension,
    Member,
    OptionType,
    Permissions,
    Role,
    SlashCommandChoice,
    SlashContext,
    slash_command,
    slash_default_member_permission,
    slash_option,
)
from interactions.client.utils import get, get_all

from core.base import CustomClient
from models import Condition, Metarole, Moderation


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

    @staticmethod
    async def __get_moderation(
        metarole_id: int, member_id: int
    ) -> Optional[Moderation]:
        return await Moderation.filter(
            member=member_id, metarole_id=metarole_id
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
    @slash_default_member_permission(Permissions.MANAGE_ROLES)
    async def metarole_add(self, ctx: SlashContext, meta_role: Role):
        metarole = await self.__get_metarole(int(ctx.guild.id), int(meta_role.id))
        if not metarole:
            await Metarole.create(
                id=int(meta_role.id), enabled=False, guild=int(ctx.guild.id)
            )
            await ctx.send("Meta-role created")
        else:
            await ctx.send(f"{meta_role.name} is already a meta-role")

    @slash_command(
        name="metarole",
        description="Meta-roles management",
        group_name="condition",
        group_description="Conditions management",
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
        description="Name of the condition role",
        required=True,
        opt_type=OptionType.ROLE,
    )
    @slash_option(
        name="condition_type",
        description="Type of the condition",
        required=True,
        opt_type=OptionType.INTEGER,
        choices=[
            SlashCommandChoice(name="Required", value=1),
            SlashCommandChoice(name="Forbidden", value=-1),
        ],
    )
    @slash_default_member_permission(Permissions.MANAGE_ROLES)
    async def metarole_condition_add(
        self,
        ctx: SlashContext,
        meta_role: Role,
        condition_role: Role,
        condition_type: int,
    ):
        metarole = await self.__get_metarole(int(ctx.guild.id), int(meta_role.id))
        condition = await self.__get_condition(
            int(meta_role.id), int(condition_role.id)
        )
        if metarole:
            if not condition:
                await Condition.create(
                    id=int(condition_role.id),
                    metarole_id=int(meta_role.id),
                    type=condition_type,
                )
                await ctx.send("Condition added")
            else:
                await ctx.send(
                    f"{condition_role.name} is already a condition for {meta_role.name}"
                )
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
    @slash_default_member_permission(Permissions.MANAGE_ROLES)
    async def metarole_condition_delete(
        self, ctx: SlashContext, meta_role: Role, condition_role: Role
    ):
        metarole = await self.__get_metarole(int(ctx.guild.id), int(meta_role.id))
        condition = await self.__get_condition(
            int(meta_role.id), int(condition_role.id)
        )
        if metarole:
            if condition:
                await condition.delete()
                await ctx.send("Condition deleted")
            else:
                await ctx.send(
                    f"{condition_role.name} is not a condition for {meta_role.name}"
                )
        else:
            await ctx.send(f"{meta_role.name} is not a meta-role")

    @slash_command(
        name="metarole",
        description="Meta-roles management",
        group_name="moderation",
        group_description="Moderation management",
        sub_cmd_name="add",
        sub_cmd_description="Add a moderation rule to a meta-role",
    )
    @slash_option(
        name="meta_role",
        description="Name of the meta-role",
        required=True,
        opt_type=OptionType.ROLE,
    )
    @slash_option(
        name="member",
        description="Name of the concerned member",
        required=True,
        opt_type=OptionType.USER,
    )
    @slash_option(
        name="condition_type",
        description="Type of the rule",
        required=True,
        opt_type=OptionType.INTEGER,
        choices=[
            SlashCommandChoice(name="Grant", value=1),
            SlashCommandChoice(name="Prevent", value=-1),
        ],
    )
    @slash_default_member_permission(Permissions.MANAGE_ROLES)
    async def metarole_moderation_add(
        self,
        ctx: SlashContext,
        meta_role: Role,
        member: Member,
        condition_type: int,
    ):
        metarole = await self.__get_metarole(int(ctx.guild.id), int(meta_role.id))
        if metarole:
            moderation = await self.__get_moderation(int(meta_role.id), int(member.id))
            if not moderation:
                await Moderation.create(
                    member=int(member.id),
                    metarole_id=int(meta_role.id),
                    type=condition_type,
                )
                await self.bot.check_metarole(metarole, [member])
                await ctx.send("Moderation rule added")
            else:
                await ctx.send(
                    f"{member.username} have already a moderation rule on {meta_role.name}"
                )
        else:
            await ctx.send(f"{meta_role.name} is not a meta-role")

    @slash_command(
        name="metarole",
        description="Meta-roles management",
        group_name="moderation",
        group_description="Moderation management",
        sub_cmd_name="delete",
        sub_cmd_description="Delete a moderation rule from a meta-role",
    )
    @slash_option(
        name="meta_role",
        description="Name of the meta-role",
        required=True,
        opt_type=OptionType.ROLE,
    )
    @slash_option(
        name="member",
        description="Name of the targeted member",
        required=True,
        opt_type=OptionType.USER,
    )
    @slash_default_member_permission(Permissions.MANAGE_ROLES)
    async def metarole_moderation_delete(
        self, ctx: SlashContext, meta_role: Role, member: Member
    ):
        metarole = await self.__get_metarole(int(ctx.guild.id), int(meta_role.id))
        moderation = await self.__get_moderation(int(meta_role.id), int(member.id))
        if metarole:
            if moderation:
                await moderation.delete()
                await self.bot.check_metarole(metarole, [member])
                await ctx.send("Moderation rule deleted")
            else:
                await ctx.send(
                    f"{member.username} don't have any moderation rule on {meta_role.name}"
                )
        else:
            await ctx.send(f"{meta_role.name} is not a meta-role")

    @slash_command(
        name="metarole",
        description="Meta-roles management",
        sub_cmd_name="enable",
        sub_cmd_description="Enable a meta-role",
    )
    @slash_option(
        name="meta_role",
        description="Name of the meta role to enable",
        required=True,
        opt_type=OptionType.ROLE,
    )
    @slash_default_member_permission(Permissions.MANAGE_ROLES)
    async def metarole_enable(self, ctx: SlashContext, meta_role: Role):
        metarole = await self.__get_metarole(int(ctx.guild.id), int(meta_role.id))
        if metarole:
            await metarole.update_from_dict({"enabled": True}).save()
            await self.bot.check_metarole(metarole, get_all(ctx.guild.members))
            await ctx.send("Meta-role enabled")
        else:
            await ctx.send(f"{meta_role.name} is not a meta-role")

    @slash_command(
        name="metarole",
        description="Meta-roles management",
        sub_cmd_name="disable",
        sub_cmd_description="Disable a meta-role",
    )
    @slash_option(
        name="meta_role",
        description="Name of the meta role to disable",
        required=True,
        opt_type=OptionType.ROLE,
    )
    @slash_default_member_permission(Permissions.MANAGE_ROLES)
    async def metarole_disable(self, ctx: SlashContext, meta_role: Role):
        metarole = await Metarole.filter(
            id=int(meta_role.id), guild=int(ctx.guild.id)
        ).get_or_none()
        if metarole:
            await metarole.update_from_dict({"enabled": False}).save()
            await ctx.send("Meta-role disabled")
        else:
            await ctx.send(f"{meta_role.name} is not a meta-role")

    @slash_command(
        name="metarole",
        description="Meta-roles management",
        sub_cmd_name="list",
        sub_cmd_description="List all meta-roles and rulesets",
    )
    @slash_default_member_permission(Permissions.MANAGE_ROLES)
    async def metarole_list(self, ctx: SlashContext):
        list_meta_roles = "**List of meta-roles**:\n\n"
        metaroles = await Metarole.filter(guild=int(ctx.guild.id))
        for metarole in metaroles:
            metarole_discord = get(ctx.guild.roles, id=metarole.id)
            list_meta_roles = (
                list_meta_roles
                + f"- **{metarole_discord.name}**, *{'enabled' if metarole.enabled else 'disabled'}*\n"
            )
            for condition in await metarole.conditions.all():
                condition_discord = get(ctx.guild.roles, id=condition.id)
                list_meta_roles = (
                    list_meta_roles
                    + f"\t- {condition_discord.name}, *{'required' if condition.type == 1 else 'forbidden'}*\n"
                )
            for moderation in await metarole.moderations.all():
                member_discord = get(ctx.guild.members, id=moderation.member)
                list_meta_roles = (
                    list_meta_roles
                    + f"\t-{member_discord.username}, *{'granted' if moderation.type == 1 else 'prevented'}*\n"
                )
        await ctx.send(list_meta_roles)

    @slash_command(
        name="metarole",
        description="Meta-roles management",
        sub_cmd_name="check",
        sub_cmd_description="Check conditions for all meta-roles and all members",
    )
    @slash_default_member_permission(Permissions.MANAGE_ROLES)
    async def metarole_check(self, ctx: SlashContext):
        members = get_all(ctx.guild.members)
        metaroles = await Metarole.filter(guild=int(ctx.guild.id))
        for metarole in metaroles:
            await self.bot.check_metarole(metarole, members)
        await ctx.send("Check finished")


def setup(bot: CustomClient):
    MetaRoleCommand(bot)
