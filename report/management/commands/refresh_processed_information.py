# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from report.report import refresh_processed_data, refresh_database
from common.functions import command_runner
from pathlib import Path


class Command(BaseCommand):
    help = refresh_processed_data.__doc__

    command_name = Path(__file__).stem

    @command_runner(command_name)
    def handle():
        refresh_processed_data()
        refresh_database()
