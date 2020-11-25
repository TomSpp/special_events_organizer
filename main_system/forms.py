from django import forms
from .models import Comment


class FilterOffersForm(forms.Form):

    EVENT_CHOICES = (
        ('BAL', 'BAL'),
        ('CHRZEST', 'CHRZEST'),
        ('JUBILEUSZ', 'JUBILEUSZ'),
        ('KOMUNIA ŚWIĘTA', 'KOMUNIA ŚWIĘTA'),
        ('POGRZEB', 'POGRZEB'),
        ('PRZYJĘCIE', 'PRZYJĘCIE'),
        ('WESELE', 'WESELE'),
        ('WIECZÓR PANIEŃSKI/KAWALERSKI', 'WIECZÓR PANIEŃSKI/KAWALERSKI'),
    )

    filtered_event = forms.ChoiceField(choices=EVENT_CHOICES, label='Uroczystość')
    filtered_location = forms.CharField(max_length=50, label='Lokalizacja')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {'body': ''}


class EstimationForm(forms.Form):
    people_amount = forms.IntegerField(max_value=1000, label='')
