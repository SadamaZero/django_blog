from django import forms
from markdown_editor.forms import MarkdownField


class BlogForm(forms.Form):
    title = forms.CharField(max_length=50)
    context = MarkdownField()
