from django import forms

from blogapp import models as blogapp_models


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = blogapp_models.Comment
        fields = ["name", "email", "body"]


class SearchForm(forms.Form):
    query = forms.CharField()
