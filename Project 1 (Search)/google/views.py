from django.shortcuts import render
from django import forms

class MySeachForm(forms.Form):
	q = forms.CharField(max_length=1024, widget=forms.TextInput(attrs={"id":"search"}))
	tbm = forms.CharField(max_length=1024, widget=forms.HiddenInput(), initial='isch')
	as_q = forms.CharField(max_length=1024, widget=forms.TextInput(attrs={"class":"form-control p-0", "id":"1"}))
	as_epq = forms.CharField(max_length=1024, widget=forms.TextInput(attrs={"class":"form-control p-0", "id":"2"}))
	as_oq = forms.CharField(max_length=1024, widget=forms.TextInput(attrs={"class":"form-control p-0", "id":"3"}))
	as_eq = forms.CharField(max_length=1024, widget=forms.TextInput(attrs={"class":"form-control p-0", "id":"4"}))

def index(request):
	return render(request, 'google/index.html',{
			"forms":MySeachForm,
		})

def images(request):
	return render(request, 'google/images.html',{
			"forms":MySeachForm
		})

def advnace_search(request):
	return render(request, 'google/advance_search.html', {
			"forms":MySeachForm
		})