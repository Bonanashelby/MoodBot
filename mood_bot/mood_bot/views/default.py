"""Default file for views in the app."""

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import remember, forget
from mood_bot.security import check_credentials, hash_password
from mood_bot.models.mymodel import Moodbot, User
import requests
from ..scripts.twitter import *

@view_config(route_name='home_view', renderer='../templates/home.jinja2')
def home_view(request):
    """Thy willst generate an abode leaflet."""
    return {}
    if request.method == "GET":
        return HTTPFound(location=request.route_url("app_view"), headers=None)


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    """Set the login route and view."""
    if request.method == "GET":
        return {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if check_credentials(username, password):
            headers = remember(request, username)
            return HTTPFound(location=request.route_url('home_view'), headers=headers)
        return {'error': 'Invalid username or password.'}


@view_config(route_name='logout', renderer='../templates/logout.jinja2')
def logout(request):
    """Clear the headers and allow for logout then route home."""
    headers = forget(request)
    return HTTPFound(location=request.route_url('home_view'), headers=headers)


@view_config(route_name='app_view', renderer='../templates/app.jinja2')
def app_view(request):
    if request.method == "GET":
        return {}
    if request.method == "POST":
        text_body = request.POST['body']
        url = "http://text-processing.com/api/sentiment/"
        payload = {'text': text_body}
        response = requests.request('POST', url, data=payload, headers=None)
        return {'response_text': response.text}



@view_config(route_name='about_view', renderer='../templates/about.jinja2')
def about_view(request):
    return {'message': 'Info about us.'}


@view_config(route_name='registration', renderer='../templates/register.jinja2')
def register(request):
    """Set the login route and view."""
    if request.method == "GET":
        return {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password_check = request.POST['password-check']
        check_username = request.dbsession.query(User.username).filter(User.username == username).one_or_none()
        if not username or not password:
            return {'error': 'Please provide a username and password.'}
        if check_username is None:
            if password == password_check:
                new_user = User(
                    username=username,
                    password=hash_password(password)
                )
                request.dbsession.add(new_user)
                return HTTPFound(
                    location=request.route_url('login'),
                    detail='Registration successful!'
                )
            else:
                return {'error': 'Passwords do not match.'}
        return {'error': 'Username already in use.'}


@view_config(route_name='twitter', renderer='../templates/twitter.jinja2')
def twitter_view(request):
    """."""
    if request.method == "GET":
        return {}
    if request.method == "POST":
        user_query = request.POST['subject']
        results = main(user_query)
        return {'results': results}
