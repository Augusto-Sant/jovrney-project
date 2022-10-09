from django import forms
from django.forms import CharField
from api.models import Journal,Page


class CreateJournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['title','description']

class EditJournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['title','description']

#

class CreatePageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['content']