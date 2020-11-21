from django.shortcuts import render
import random
import markdown2

from . import util
entries = util.list_entries()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "random": random.choice(entries)
    })
    
def add(request):
    return render(request, "encyclopedia/add.html", {
        "entries": entries,
        "random": random.choice(entries)
    })
    
def entry(request, title):
    entry = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown2.markdown(entry),
        "random": random.choice(entries)
       })
