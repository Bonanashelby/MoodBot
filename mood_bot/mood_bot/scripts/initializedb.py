"""Intialize Database file."""

import os
import random
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
from mood_bot.models import User
from mood_bot.models.mymodel import Sentiments
from faker import Faker
from passlib.apps import custom_app_context as context


fake_data = Faker()
FAKE_DATA = [{'body': fake_data.text(), 'negative_sentiment': faker.random.random(), 'positive_sentiment': faker.random.random(), 'user_id': random.randint(1, 3)} for i in range(20)]

FAKE_USER =[{'username': 'turbo', 'password': context.hash('maple')}, 
            {'username': 'kitties', 'password': context.hash('fluff')},
            {'username': 'tree', 'password': context.hash('leafy')}]

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

        faker_user = []
        for fake in FAKE_USER:
            even_newer_result = User(
                username=fake['username'],
                password=fake['password']
            )
            faker_user.append(even_newer_result)
        dbsession.add_all(faker_user)


        faker_models = []
        for fake in FAKE_DATA:
            newer_result = Sentiments(
                body=fake['body'],
                negative_sentiment=fake['negative_sentiment'],
                positive_sentiment=fake['positive_sentiment'],
                user_id=fake['user_id']
            )
            faker_models.append(newer_result)
        dbsession.add_all(faker_models)

