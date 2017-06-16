"""Default file for views in the app."""
import requests
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import remember, forget
from mood_bot.security import check_credentials, hash_password
from mood_bot.models.mymodel import User, Sentiments
import json
from ..scripts.twitter import *


@view_config(route_name='home_view', renderer='../templates/home.jinja2')
def home_view(request):
    """Thy willst generate an abode leaflet."""
    if request.authenticated_userid:
        return HTTPFound(location=request.route_url('app_view'))  # pragma no cover
    return {} # pragma no cover


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    """Log users in in order to use moodbot."""
    if request.method == "GET":
        return {}
    if request.method == "POST":
        if check_credentials(request):
            username = request.POST['username']
            headers = remember(request, username)
            return HTTPFound(location=request.route_url('home_view'), headers=headers) 
        return {'error': 'Invalid username or password.'}


@view_config(route_name='logout', renderer='../templates/logout.jinja2')
def logout(request):
    """Clear the headers and allow for logout then route home."""
    headers = forget(request)
    return HTTPFound(location=request.route_url('home_view'), headers=headers)


@view_config(route_name='app_view', renderer='../templates/app.jinja2', permission='secret')
def app_view(request):
    """COnducts the bulk of our bot functionality."""
    prior_queries = (request.dbsession.query(Sentiments, User)
                                      .join(User)
                                      .filter(User.username == request.authenticated_userid)
                                      .order_by(Sentiments.id.desc())
                                      .all())
    sentient_bodies = (query[0].body for query in prior_queries)
    sentimental_parts = (percentage(query[0].negative_sentiment) for query in prior_queries)
    logical_bits = (percentage(query[0].positive_sentiment) for query in prior_queries)
    sublime_insight = zip(sentient_bodies, sentimental_parts, logical_bits)
    if request.method == "POST":
        text_body = request.POST['body']
        url = "http://text-processing.com/api/sentiment/"
        payload = {'text': text_body}
        response = requests.request('POST', url, data=payload, headers=None)
        response_dict = json.loads(response.text)
        user_query = request.dbsession.query(User).filter(User.username == request.authenticated_userid).one().id
        sentiment_entry = Sentiments(
            body=text_body,
            negative_sentiment=response_dict['probability']['neg'],
            positive_sentiment=response_dict['probability']['pos'],
            user_id=user_query
        )
        request.dbsession.add(sentiment_entry)
        response_dict['probability']['neg'] = percentage(response_dict['probability']['neg'])
        response_dict['probability']['pos'] = percentage(response_dict['probability']['pos'])
        return {'response_dict': response_dict,
                'text_body': text_body,
                'consummate_awareness': sentient_bodies,
                'conscious whole': sentimental_parts,
                'divine oneness': logical_bits,
                'hallowed_provenance': sublime_insight}
    return {'consummate_awareness': sentient_bodies,
            'conscious whole': sentimental_parts,
            'divine oneness': logical_bits,
            'hallowed_provenance': sublime_insight}


@view_config(route_name='about_view', renderer='../templates/about.jinja2')
def about_view(request):
    """Display a page about the team."""
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


@view_config(route_name='twitter', renderer='../templates/twitter.jinja2', permission='secret')
def twitter_view(request):
    """Extract tweets."""
    if request.method == "GET":
        return {}
    if request.method == "POST":
        user_query = request.POST['subject']
        results = main(user_query)
        return {'results': results}
