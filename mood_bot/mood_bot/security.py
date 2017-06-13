"""Security configuration for our Pyramid application."""
import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Authenticated, Allow
from passlib.apps import custom_app_context as context
from pyramid.session import SignedCookieSessionFactory
from mood_bot.models.mymodel import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists


class MyRoot(object):

    def __init__(self, request):
        """The init for security."""
        self.request = request

    __acl__ = [
        (Allow, Authenticated, 'secret')
    ]


def check_credentials(username, password):
    """Check credentials of a new user.
    Return True if it checks out; otherwise return False."""
    engine = create_engine('postgres://kurtrm:hofbrau@localhost:5432/mood_bot')
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    stored_username = session.query(User.username).filter(User.username==username)
    username_existence = session.query(stored_username.exists()).scalar()
    if not username_existence:
        return False
    stored_username = stored_username.first().username
    stored_password = session.query(User.password).filter(User.username==stored_username).first().password
    return context.verify(password, stored_password)


def hash_password(password):
    """Hash the new user's password."""
    return context.hash(password)


def includeme(config):
    """Configuration for security."""
    auth_secret = os.environ.get('AUTH_SECRET', '')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(MyRoot)
    session_secret = os.environ.get('SESSION_SECRET', '')
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)
    config.set_default_csrf_options(require_csrf=False)
    