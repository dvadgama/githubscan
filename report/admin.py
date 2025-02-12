# -*- coding: utf-8 -*-
from django.contrib import admin
from report.models import (
    Team,
    TeamNotificationTarget,
    OrganizationNotificationTarget,
    EnterpriseUser,
    SAMLNotificationTarget,
)


@admin.register(EnterpriseUser)
class EnterpriseUserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "login")


@admin.register(TeamNotificationTarget)
class TeamNotificationTargetAdmin(admin.ModelAdmin):
    list_display = ("get_team_name", "email", "red_alerts_only")

    def get_team_name(self, obj):
        return obj.team.name

    get_team_name.short_description = "Team"
    get_team_name.admin_order_field = "team__name"


@admin.register(SAMLNotificationTarget)
class SAMLNotificationTargetAdmin(admin.ModelAdmin):
    list_display = ("get_team_name", "login", "email", "red_alerts_only")

    def get_team_name(self, obj):
        return obj.team.name

    get_team_name.short_description = "Team"
    get_team_name.admin_order_field = "team__name"


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "reporting_enabled")


@admin.register(OrganizationNotificationTarget)
class OrganizationNotificationTargetAdmin(admin.ModelAdmin):
    list_display = ("email", "reporting_enabled")
