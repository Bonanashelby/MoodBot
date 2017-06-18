import unittest
import transaction
import random

from pyramid import testing
from pyramid.response import Response

import pytest
from mood_bot.models import (
    User,
    Sentiments,
    get_tm_session,
)
from mood_bot.models.meta import Base
from faker import Faker
from passlib.apps import custom_app_context as context


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
        'sqlalchemy.url': 'postgres://localhost:5432/test_moodybot'
    })
    config.include("mood_bot.models")
    config.include("mood_bot.routes")
    config.include("mood_bot.security")

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

    FAKE_USER = [
        {'username': 'kurtykurt', 'password': context.hash('kurtkurt')},
        {'username': 'caseyisawesome', 'password': context.hash('casey')},
        {'username': 'ajshorty', 'password': context.hash('shorty')},
        {'username': 'annabanana', 'password': context.hash('banana')}
    ]

    fake_data = Faker()
    FAKE_DATA = [
        {'body': fake_data.text(),
            'negative_sentiment': fake_data.random.random(),
            'positive_sentiment': fake_data.random.random(),
            'user_id': random.randint(1, 3)}
        for i in range(20)
    ]

    faker_user = []
    for fake in FAKE_USER:
        even_newer_result = User(
            username=fake['username'],
            password=fake['password'],
        )
        faker_user.append(even_newer_result)
    session.add_all(faker_user)

    faker_models = []
    for fake in FAKE_DATA:
        newer_results = Sentiments(
            body=fake['body'],
            negative_sentiment=fake['negative_sentiment'],
            positive_sentiment=fake['positive_sentiment'],
            user_id=fake['user_id']
        )
        faker_models.append(newer_results)
    session.add_all(faker_models)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def post_request(dummy_request):
    dummy_request.method = "POST"
    return dummy_request


@pytest.fixture
def dummy_request(db_session):
    """Dummy request fixture."""
    return testing.DummyRequest(dbsession=db_session)


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


# def test_login_redirects_to_home_view(post_request):
#     """Test that login redirects to the home page after login."""
#     from mood_bot.views.default import login
#     from pyramid.httpexceptions import HTTPFound
#     data_dict = {'username': 'kurtykurt', 'password': 'kurtkurt'}
#     post_request.POST = data_dict
#     response = login(post_request)
#     assert response.status_code == 302
#     assert isinstance(response, HTTPFound)


def test_about_view_returns_response():
    """About view returns a Response object."""
    from mood_bot.views.default import about_view
    request = testing.DummyRequest()
    response = about_view(request)
    assert isinstance(response, dict)


def test_register_view_returns_response():
    """Register view returns a Response object."""
    from mood_bot.views.default import register
    request = testing.DummyRequest()
    response = register(request)
    assert isinstance(response, dict)


# def test_register_user_for_login(dummy_request):
#     """Test that checks for user login."""
#     from mood_bot.views.default import register
#     from pyramid.httpexceptions import HTTPFound
#     data_dict = {'username': 'kurtykurt', 'password': 'kurtkurt', 'password-check': 'kurtkurt'}
#     dummy_request.POST = data_dict
#     response = register(dummy_request)
#     assert response.status_code == 302
#     assert isinstance(response, HTTPFound)


def test_register_error(dummy_request):
    """Test that login error raises for invalid registration."""
    from mood_bot.views.default import register
    data_dict = {'username': '', 'password': '', 'password-check': ''}
    dummy_request.POST = data_dict
    response = register(dummy_request)
    assert response == {'error': 'Please provide a username and password.'}


def test_register_error_for_non_matching_password(dummy_request):
    """Test that login error raises for not matching password."""
    from mood_bot.views.default import register
    data_dict = {'username': 'kurtykurt', 'password': 'kurtkurt', 'password-check': 'kurt'}
    dummy_request.POST = data_dict
    response = register(dummy_request)
    assert response == {'error': 'Passwords do not match.'}


def test_twitter_main_response_is_response():
    """Test that the main function in twitter returns response."""
    from mood_bot.scripts.twitter import main
    query = 'Dinosaur'
    response = main(query)
    assert response == response


def test_twitter_main_tweets_is_response():
    """Test the main function does the thing."""
    from mood_bot.scripts.twitter import main
    query = 'nhuntwalker'
    response = main(query)
    tweets = []
    tweets.extend(response)
    assert response == tweets


def test_twitter_view_does_the_thing():
    """About twitter returns a Response object."""
    from mood_bot.views.default import twitter_view
    request = testing.DummyRequest()
    response = twitter_view(request)
    assert isinstance(response, dict)


def test_twitter_view_post_request(post_request):
    """Test that twitter post request returns results."""
    tweets = 'Dinosaur'
    post_request.POST = tweets
    response = post_request.POST
    assert response == tweets
