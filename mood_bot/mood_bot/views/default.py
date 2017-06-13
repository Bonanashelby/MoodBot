"""Default file for views in the app."""

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import remember, forget
from mood_bot.security import check_credentials
import datetime
import json
import requests


@view_config(route_name='home_view', renderer='../templates/home.jinja2')
def home_view(request):
    return {
        'test': 'Testing'
    }


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login():
    pass


@view_config(route_name='logout', renderer='../templates/logout.jinja2')
def logout():
    pass


@view_config(route_name='app_view', renderer='../templates/app.jinja2')
def app_view():
    pass


@view_config(route_name='results', renderer='../templates/results.jinja2')
def results_view(request):
    pass


@view_config(route_name='about_view', renderer='../templates/about.jinja2')
def about_view():
    pass


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
