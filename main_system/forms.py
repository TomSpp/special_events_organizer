from django import forms
from .models import Comment


class FilterOffersForm(forms.Form):
    VOIVODESHIP_CHOICES = (
        ('1', 'dolnośląskie'),
        ('2', 'mazowieckie'),
    )

    filtered_location = forms.CharField(max_length=50, label='')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
