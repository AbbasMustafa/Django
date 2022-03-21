from django import forms 
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post']

        widgets = {
            'post': forms.Textarea(attrs={'cols': 40, 'rows': 3,
            						 'class':'form-control',
            						 'placeholder':'Add a post.'}),
        }
		