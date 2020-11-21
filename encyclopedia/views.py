from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect

import random
import markdown2

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Markdown Content", max_length=50000, widget=forms.Textarea(attrs={'class' : 'test'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "random": random.choice(util.list_entries())
    })
    
def add(request):
    if request.method == "POST":   
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            util.save_entry(title, content)
            return HttpResponseRedirect(f"{title}")
        else:
            return render (request, "encyclopedia/add.html", {
                "form": form
            })
    
    return render(request, "encyclopedia/add.html", {
        "entries": util.list_entries(),
        "form": NewEntryForm(),
        "random": random.choice(util.list_entries())
    })
    
def entry(request, title):
    entry = util.get_entry(title)    
    
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown2.markdown(entry),
        "random": random.choice(util.list_entries())
       })
