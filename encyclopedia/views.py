from django.shortcuts import render
from django import forms
from django.views.generic import ListView
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, HttpResponse 
from django.urls import reverse
from . import util
import random
import markdown2

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Markdown Content", max_length=50000, widget=forms.Textarea())
class EditEntryForm(forms.Form):
    content = forms.CharField(label="Markdown Content", max_length=50000, widget=forms.Textarea())
class SearchForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Entries', 'style': 'width:100%'}))
    
def index(request):    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm(),
        "random": random.choice(util.list_entries())
    })

def search(request):     
    if request.method == "POST":
        results = [] # new empty results list
        entries = util.list_entries() # populated with ALL entries
        form = SearchForm(request.POST)
        
        if form.is_valid():
            query = form.cleaned_data["query"]
            for entry in entries:
                # Check for exact match & redirect
                if query.lower() == entry.lower():
                    title = entry
                    entry = util.get_entry(title)
                    return render(request, "encyclopedia/entry.html", {
                    "entry": markdown2.markdown(entry),
                    "random": random.choice(util.list_entries()),
                    "form": SearchForm()
                })
                # Check for partial matches
                if query.lower() in entry.lower():
                    results.append(entry)
            
            # Returns partial matches to results
            return render(request, "encyclopedia/search.html", {
            "results": results,
            "query": query,
            "form": SearchForm(),
            "random": random.choice(util.list_entries())
           })
        
        return render(request, 'encyclopedia/search.html', {
            'entries': entries, 
            'query': query
        })
    # Returns empty values   
    return render(request, 'encyclopedia/search.html', {
        "results": "", 
        "query": "",
        "form": SearchForm(),
        "random": random.choice(util.list_entries())
    })
    
def entry(request, title):
    entry = util.get_entry(title)    
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(entry),
            "random": random.choice(util.list_entries()),
            "form": SearchForm()
           })
    return render(request, "encyclopedia/error.html", {
        "random": random.choice(util.list_entries()),
        "form": SearchForm()
    })
    
def add(request):
    entryform = NewEntryForm(request.POST)
    if request.method == "POST":   
        if entryform.is_valid():
            title = entryform.cleaned_data["title"]
            content = entryform.cleaned_data["content"]
            if not title.lower() in util.list_entries():
                util.save_entry(title, content)
                return render(request, "encyclopedia/entry.html", {
                    "entry": markdown2.markdown(content),
                    "random": random.choice(util.list_entries()),
                    "form": SearchForm()
                })
            else:
                return render (request, "encyclopedia/add.html", {
                    "form": SearchForm(),
                    "entryform": entryform,
                    "error": "Error: An entry with this title already exists."
                })    
        else:
            return render (request, "encyclopedia/add.html", {
                "form": SearchForm(),
                "entryform": entryform
            })
    
    return render(request, "encyclopedia/add.html", {
        "form": SearchForm(),
        "entries": util.list_entries(),
        "random": random.choice(util.list_entries()),
        "entryform": entryform,
    })
    
def edit(request):
    title = request.META['HTTP_REFERER'].strip("http://127.0.0.1:8000/wiki/")
    content = util.get_entry(title)  
    
    if request.method == "POST":   
        editform = EditEntryForm(request.POST)
        if editform.is_valid():
            content = editform.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                    "entry": markdown2.markdown(content),
                    "random": random.choice(util.list_entries()),
                    "form": SearchForm()
                })

        else:
            return render (request, "encyclopedia/edit.html", {
                "editform": form,
                "form": SearchForm()
            })

    return render(request, "encyclopedia/edit.html", {
        "entries": util.list_entries(),
        "random": random.choice(util.list_entries()),
        "editform": EditEntryForm(initial={'title':title,'content':content}),
        "form": SearchForm()
    })