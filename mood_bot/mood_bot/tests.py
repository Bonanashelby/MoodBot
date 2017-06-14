import unittest
import transaction

from pyramid import testing
from pyramid.response import Response

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
        'sqlalchemy.url': 'postgres:///moodybot'
    })
    config.include("mood_bot.models")
    config.include("mood_bot.routes")

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


@pytest.fixture
def dummy_request(db_session):
    """Dummy request fixture."""
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture(scope="session")
def testapp(request):
    """Testapp."""
    from webtest import TestApp
    from mood_bot import main

    app = main({}, **{"sqlalchemy.url": "postgres:///moodybot"})
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tearDown)

    return testapp


def test_home_view_returns_response():
    """Home view returns a Response object."""
    from mood_bot.views.default import home_view
    request = testing.DummyRequest()
    response = home_view(request)
    assert isinstance(response, dict)


def test_login_view_returns_response():
    """Login view returns a Response object."""
    from mood_bot.views.default import login
    request = testing.DummyRequest()
    response = login(request)
    assert isinstance(response, dict)


def test_login_error(dummy_request):
    """Test error for login."""
    from mood_bot.views.default import login
    dummy_request.method = "POST"
    data_dict = {'username': 'thisismylogin', 'password': 'notmypassword'}
    dummy_request.POST = data_dict
    response = login(dummy_request)
    assert response == {'error': 'Invalid username or password.'}


# def test_login_redirects_to_home_view(dummy_request):
#     """Test that login redirects to the home page after login."""
#     from mood_bot.views.default import login
#     dummy_request.method = "POST"
#     data_dict = {'username': 'kurtykurt', 'password': 'kurtkurt'}
#     dummy_request.POST = data_dict
#     response = login(dummy_request)
#     assert response.status_code == 302 


def test_about_view_returns_response():
    """about view returns a Response object."""
    from mood_bot.views.default import about_view
    request = testing.DummyRequest()
    response = about_view(request)
    assert isinstance(response, dict)


def test_register_view_returns_response():
    """register view returns a Response object."""
    from mood_bot.views.default import register
    request = testing.DummyRequest()
    response = register(request)
    assert isinstance(response, dict)


# def test_response_200_about_view():
#     pass


# def test_response_200_app_view():
#     pass


# def test_response_200_login():
#     pass
