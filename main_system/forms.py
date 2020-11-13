from django import forms


class FilterOffersForm(forms.Form):
    VOIVODESHIP_CHOICES = (
        ('1', 'dolnośląskie'),
        ('2', 'mazowieckie'),
    )

    filtered_location = forms.CharField(max_length=50, label='')
