from django import forms
from django.forms import ModelForm
from main.models import Shoes, ShoeSize, SIZE_CHOICES

class ShoesForm(ModelForm):
    class Meta:
        model = Shoes
        fields = ["name", "price", "description", "thumbnail"]

class OneSizeForm(forms.Form):
    size = forms.ChoiceField(choices=SIZE_CHOICES, required=True, label="Shoe size")
    stock = forms.IntegerField(min_value=0, required=True, label="Jumlah/Stock")
