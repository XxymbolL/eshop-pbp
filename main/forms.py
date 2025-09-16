from django.forms import ModelForm
from main.models import Shoes

class ShoesForm(ModelForm):
    class Meta:
        model = Shoes
        fields = ["name", "price", "description", "thumbnail"]
