import unittest
import transaction

from pyramid import testing


import pytest
from mood_bot.models import (
    Moodbot,
    get_tm_session,
)
from mood_bot.models.meta import Base


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.

    This Configurator instance sets up a pointer to the location of the
        database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.

    This configuration will persist for the entire duration of your PyTest run.
    """
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres:///test_moodbot'
    })
    config.include("mood_bot.models")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a session for interacting with the test database.

    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


def test_model_gets_added(db_session):
    assert len(db_session.query(Expense).all()) == 0
    model = Expense(
        category="Fake Category",
        description="Some description text",
        creation_date=datetime.datetime.now(),
        amount=12345.67
    )
    db_session.add(model)
    assert len(db_session.query(Expense).all()) == 1


def test_response_200_home_view():



# def test_response_200_about_view():
#     pass


# def test_response_200_app_view():
#     pass


# def test_response_200_login():
#     pass
