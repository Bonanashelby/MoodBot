"""Default file for views in the app."""

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import remember, forget
from mood_bot.security import check_credentials
from mood_bot.models.mymodel import Moodbot
import requests


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
        text = request.POST['body']


@view_config(route_name='about_view', renderer='../templates/about.jinja2')
def about_view(request):
    return {'message': 'Info about us.'}



@view_config(route_name="results", renderer='../templates/results.jinja2')
def result_view(request):
    """View of the result route."""
    the_id = int(request.matchdict['id'])
    results = request.dbsession.query(Moodbot).get(the_id)
    if results:
        return {
            "score": results.score,
            "explain_score": results.explain_score
        }
    else:
        raise HTTPNotFound


@view_config(route_name='entry', renderer='../templates/entry.jinja2')
def test_api_stuff(request):
    if request.method == "GET":
        return {}
    if request.method == "POST":
        text_body = request.POST['body']
        url = "http://text-processing.com/api/sentiment/"
        payload = {'text': text_body}
        response = requests.request('POST', url, data=payload, headers=None)
        return {'response_text': response.text}
