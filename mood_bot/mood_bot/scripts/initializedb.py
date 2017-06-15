"""Intialize Database file."""

import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)
from mood_bot.models import Moodbot
from mood_bot.models.mymodel import User
from faker import Faker


fake_data = Faker()
FAKE_DATA = [{'body': fake_data.text(), 'sentiment': fake_data.boolean(), 'user_id': fake.random_number(1)} for i in range(20)]


def usage(argv):
    """."""
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(exMample: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    """."""
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

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)


        faker_models = []
        for fake in FAKE_DATA:
            newer_result = Sentiment(
                body=fake['body'],
                sentiment=fake['sentiment'],
                fake_data=fake['user_id']
            )
            faker_models.append(newer_result)
        dbsession.add_all(faker_models)


        dbsession.add(User())

