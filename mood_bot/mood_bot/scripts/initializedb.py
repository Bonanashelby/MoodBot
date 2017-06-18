"""Intialize Database file."""

import os
import sys
from pyramid.paster import (
    get_appsettings,
    setup_logging,
)
from pyramid.scripts.common import parse_vars
from ..models.meta import Base
from ..models import get_engine


def usage(argv):
    """."""
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(exMample: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    """Define the Database to use on the command line."""
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    settings["sqlalchemy.url"] = os.environ["DATABASE_URL"]
    engine = get_engine(settings)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
