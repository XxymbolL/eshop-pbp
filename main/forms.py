from django import forms
from django.forms import ModelForm, inlineformset_factory, BaseInlineFormSet
from main.models import Shoes, ShoeSize

class ShoesForm(ModelForm):
    class Meta:
        model = Shoes
        fields = ["name", "price", "description", "thumbnail"]

class ShoeSizeForm(ModelForm):
    class Meta:
        model = ShoeSize
        fields = ["size", "stock"]
        labels = {"size": "Shoe size", "stock": "Jumlah/Stock"}

class BaseShoeSizeFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        seen = set()
        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue
            if self.can_delete and form.cleaned_data.get("DELETE"):
                continue
            size = form.cleaned_data.get("size")
            stock = form.cleaned_data.get("stock")
            if size in (None, "") and stock in (None, ""):
                continue
            if size in seen:
                form.add_error("size", "Duplicate size in this product.")
            else:
                seen.add(size)

SizeFormSet = inlineformset_factory(
    Shoes,
    ShoeSize,
    form=ShoeSizeForm,
    formset=BaseShoeSizeFormSet,
    extra=3,
    can_delete=True,
    min_num=1,
    validate_min=True,
    max_num=15,
)
