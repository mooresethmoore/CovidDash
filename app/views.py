"""
Definition of views.
"""
import os
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
import json
from json import load
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    map={}
    cstates={}
    #rs=json.loads(open("C:/Code/git/proj/CovidDash/CovidDash/app/static/app/covidStates.json").read())
    #print(['Alabama' in rs[d] for d in rs.keys()])
    
#    with open("C:/Code/git/proj/CovidDash/CovidDash/app/static/app/content/usaMainland.json") as f:
#        map.update(load(f))
#    with open("C:/Code/git/proj/CovidDash/CovidDash/app/static/app/covidStates.json") as f:
#        cstates.update(load(f))
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with open("static/app/content/usaMainland.json") as f:
        map.update(load(f))
    with open("static/app/covidStates.json") as f:
        cstates.update(load(f))


    return render(
        request,
        'app/home.html',
        {
           'title':'COVID-19 Statewide Tracking',
           'year':datetime.now().year,
           'usmap':map,
            'covidStates':cstates
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
