from django.shortcuts import render
from django import forms
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

import random
import markdown2

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Markdown Content", max_length=50000, widget=forms.Textarea())
class EditEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Markdown Content", max_length=50000, widget=forms.Textarea())
class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput)

def index(request):
    """query = request.GET.get['q']"""
    entries = util.list_entries()
    results = []
    
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data()
    
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "random": random.choice(entries)
    })
    
def add(request):
    form = NewEntryForm(request.POST)
    if request.method == "POST":   
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if not title in util.list_entries():
                util.save_entry(title, content)
                return HttpResponseRedirect(f"{title}")
            else:
                return render (request, "encyclopedia/add.html", {
                    "form": form,
                    "error": "Error: An entry with this title already exists."
                })    
        else:
            return render (request, "encyclopedia/add.html", {
                "form": form
            })
    
    return render(request, "encyclopedia/add.html", {
        "entries": util.list_entries(),
        "random": random.choice(util.list_entries()),
        "form": NewEntryForm(),
    })
    
def edit(request):
    title = request.META['HTTP_REFERER'].strip("http://127.0.0.1:8000/wiki/")
    content = util.get_entry(title)  
    
    if request.method == "POST":   
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            util.save_entry(title, content)
            return HttpResponseRedirect(f"{title}")

        else:
            return render (request, "encyclopedia/edit.html", {
                "form": form
            })

    return render(request, "encyclopedia/edit.html", {
        "entries": util.list_entries(),
        "random": random.choice(util.list_entries()),
        "form": EditEntryForm(initial={'title':title,'content':content}),
    })
    
def entry(request, title):
    entry = util.get_entry(title)    
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(entry),
            "random": random.choice(util.list_entries())
           })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "random": random.choice(util.list_entries())
    })
    

def search(request, query):  
    query = request.GET["q"]
    entries = util.list_entries()
    results = []
    
    if util.get_entry(query):
        return entry
        
    elif request.method == 'GET':
        return render(request, 'encyclopedia/search.html', {
            'entries': entries, 
            'query': query
        })
        
    return render(request, "encyclopedia/index.html", {
        
    })