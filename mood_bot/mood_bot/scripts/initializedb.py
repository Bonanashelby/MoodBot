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


RESULTS = [
    {
        "body": "This is a test of results.",
        "score": 0.7,
        "explain_score": "This is an explaination of the scoring results."

    }
]


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

    engine = get_engine(settings)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        many_models = []
        for item in RESULTS:
            new_result = Moodbot(
                body=item['body'],
                score=item['score'],
                explain_score=item['explain_score']
            )
            many_models.append(new_result)
        dbsession.add_all(many_models)

        model = Moodbot()
        dbsession.add(model)
        dbsession.add(User())
