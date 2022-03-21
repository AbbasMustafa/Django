from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import secrets
from markdown2 import Markdown
from . import util

# Index Page
# This page shows all available entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Entry Page
# This page shows individual entry and it's content which user wants
def entry_view(request, entry):
	entryPage = util.get_entry(entry)
	markdowner = Markdown()
	# Check if requested entry is available in entry list or not!
	if entryPage is None:
		return render(request, 'encyclopedia/PageNotExist.html',{
					"entry":entry,
			})
	else:
		return render(request, 'encyclopedia/entry.html',{
				"entry":markdowner.convert(entryPage),
				"entryTitle":entry,
				"form":CreateEntryForm,
			})

# Search Entry
# This view is for users to search their desire page using search bar
def search(request):
	subStringEntries = []
	entry = request.GET.get('q')
	# Check if requested entry is in entires or Not!
	if util.get_entry(entry) is not None:
		return HttpResponseRedirect(reverse('entry_view', args=(entry,)))
	else:
		# Finding Substring of requested Entry
		for list_entry in util.list_entries():
			if entry.lower() in list_entry.lower():
				subStringEntries.append(list_entry)
		if subStringEntries:
			return render(request, 'encyclopedia/list.html',{
				"entries":subStringEntries,
				})
		else:
			return HttpResponseRedirect(reverse('entry_view', args=(entry,)))

class CreateEntryForm(forms.Form):
	entryTitle = forms.CharField(widget=forms.TextInput(attrs={"id":"title",
												"class":"form-control"}))
	entryContent = forms.CharField(widget=forms.Textarea(attrs={"rows":7, 
												"id":"content","class":"form-control"}))
	editContent = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

# Create Entry
# This view will provide user to page where they create their own entry
def create(request):
	# Collect Data From Title and Content Fields
	if request.method == "POST":
		form = CreateEntryForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['entryTitle']
			content = form.cleaned_data['entryContent']
			# Check if new entry is already exist in our list or Not!
			# Or user request for Edit!
			if (util.get_entry(title) is None)  or (form.cleaned_data['editContent'] is True):
				util.save_entry(title, content.replace("\n",""))
				return HttpResponseRedirect(reverse("entry_view", args=(title,)))	
			else:
				return render(request, 'encyclopedia/CreatePage.html',{
					"form":form,
					"existing":True,
					"title":title,
				})
		else:
			return render(request, 'encyclopedia/CreatePage.html',{
					"form":form,
				})
	# if page is requested as a GET method!
	return render(request, 'encyclopedia/CreatePage.html',{
			"form":CreateEntryForm,
		})

# Edit entry
# This view is for edit any entry user wants
def edit(request, entry):
	entryContent = util.get_entry(entry)
	form = CreateEntryForm()
	form.fields['entryTitle'].initial = entry
	form.fields['entryTitle'].widget = forms.HiddenInput()
	form.fields['entryContent'].initial = entryContent
	form.fields['editContent'].initial = True
	return render(request, 'encyclopedia/CreatePage.html',{
			"form":form,
			"edit":True,
			"title":entry
		})

# Random view
# When user click Random Page link it'l redirect to random entry
def random_view(request):
	entries = util.list_entries()
	entry = secrets.choice(entries)
	return HttpResponseRedirect(reverse("entry_view", args=(entry,)))