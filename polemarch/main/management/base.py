# pylint: disable=no-member,invalid-name,broad-except
from __future__ import absolute_import, unicode_literals
import logging
import sys

from django.core.management.base import (BaseCommand,
                                         CommandError as CommandErrorBase)
from django.conf import settings
import django

from ... import __version__
from ..utils import exception_with_traceback

logger = logging.getLogger("polemarch")


class CommandError(CommandErrorBase):
    pass


class ServiceCommand(BaseCommand):
    requires_system_checks = False
    keep_base_opts = False
    stdout, stderr = sys.stdout, sys.stderr

    def add_arguments(self, parser):
        super(ServiceCommand, self).add_arguments(parser)
        parser.add_argument(
            '-l', '--log-level',
            action='store',
            dest='log-level',
            default=False,
            type=str,
            help='Set logs level [debug|warning|error|critical]')

    @exception_with_traceback()
    def handle(self, *args, **options):
        LOG_LEVEL = settings.LOG_LEVEL
        if options.get('log-level', False):
            LOG_LEVEL = options.get('log-level', LOG_LEVEL)  # pragma: no cover
        logger.setLevel(LOG_LEVEL.upper())
        self.LOG_LEVEL = LOG_LEVEL.upper()

    def get_version(self):
        return u'IHService {c}, Django {d.__version__}'.format(
            c=__version__, d=django,
        )

    def _print(self, info=""):
        self.stdout.write(str(info))  # pragma: no cover

    def _success(self, info=""):
        try:  # pragma: no cover
            self._print(self.style.SUCCESS(info))
        except:
            self._print(self.style.MIGRATE_SUCCESS(info))

    def _info(self, info=""):
        self._print(self.style.HTTP_INFO(info))

    def _error(self, info=""):
        self._print(self.style.ERROR(info))

    def _warning(self, info=""):
        self._print(self.style.WARNING(info))
