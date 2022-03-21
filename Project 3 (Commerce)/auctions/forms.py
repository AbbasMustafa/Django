from django.forms import ModelForm, TextInput, NumberInput, Select
from auctions.models import Listing, Picture, Bid

class ListingForm(ModelForm):
	class Meta:
		model = Listing
		fields = ['title','description','startingBid','category']

		widgets = {
			"title": TextInput(attrs={'class':"form-control",
											"id":"title"}),
			"description": TextInput(attrs={'class':"form-control",
											"id":"desc"}),
			"startingBid": NumberInput(attrs={'class':"form-control",
											"id":"price"}),
			"category": Select(attrs={'class':"form-control",
											"id":"category"}),
		}
	
class PictureForm(ModelForm):
	class Meta:
		model = Picture
		fields = ['picture']

class BidForm(ModelForm):
	class Meta:
		model = Bid
		fields = ['offer']

		widgets = {
			"offer": NumberInput(attrs={"class":"bidInput"})
		}